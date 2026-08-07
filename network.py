"""
Terminal Pet Society - P2P Network Layer
Enables pets to visit each other across the local network using TCP.
Uses a simple discovery + connection protocol.
"""

import asyncio
import json
import socket
import threading
import time
from typing import Optional, Callable

# Protocol constants
DEFAULT_PORT = 19997  # "PETS" on a phone keypad :)
DISCOVERY_MULTICAST_ADDR = "224.0.0.199"
DISCOVERY_MULTICAST_PORT = 19998
DISCOVERY_MESSAGE = b"PET_SOCIETY_DISCOVER"
DISCOVERY_RESPONSE = b"PET_SOCIETY_HERE"


def get_local_ip() -> str:
    """Get the local network IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


class PetServer:
    """TCP server that accepts visiting pets."""
    
    def __init__(self, pet_data_provider: Callable[[], Optional[dict]],
                 on_visitor: Callable[[dict], None],
                 on_disconnect: Callable[[str], None],
                 port: int = DEFAULT_PORT):
        self.pet_data_provider = pet_data_provider
        self.on_visitor = on_visitor
        self.on_disconnect = on_disconnect
        self.port = port
        self.server: Optional[asyncio.AbstractServer] = None
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
    
    async def _handle_client(self, reader: asyncio.StreamReader,
                              writer: asyncio.StreamWriter):
        """Handle an incoming pet visitor."""
        addr = writer.get_extra_info('peername')
        
        try:
            # Receive visitor's pet data
            data = await asyncio.wait_for(reader.read(16384), timeout=5.0)
            if not data:
                return
            
            visitor_data = json.loads(data.decode())
            visitor_name = visitor_data.get("name", "Unknown")
            
            # Send our pet data back
            local_data = self.pet_data_provider()
            if local_data:
                response = json.dumps({
                    "type": "welcome",
                    "pet": local_data,
                }).encode()
                writer.write(response)
                await writer.drain()
            
            # Register visitor
            self.on_visitor(visitor_data)
            
            # Keep connection open for messages
            while self.running:
                try:
                    msg = await asyncio.wait_for(reader.read(4096), timeout=30.0)
                    if not msg:
                        break
                except asyncio.TimeoutError:
                    continue
            
        except (asyncio.TimeoutError, ConnectionError, json.JSONDecodeError):
            pass
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            if 'visitor_data' in locals():
                self.on_disconnect(visitor_data.get("name", "Unknown"))
    
    async def _run_server(self):
        self.server = await asyncio.start_server(
            self._handle_client, "0.0.0.0", self.port
        )
        self.running = True
        async with self.server:
            await self.server.serve_forever()
    
    def _thread_main(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._run_server())
        except Exception:
            pass
    
    def start(self):
        """Start the server in a background thread."""
        if self.running:
            return
        self._thread = threading.Thread(target=self._thread_main, daemon=True)
        self._thread.start()
        time.sleep(0.3)  # Give it a moment to start
    
    def stop(self):
        """Stop the server."""
        self.running = False
        if self.server:
            # Schedule server close on the event loop
            if self._loop and self._loop.is_running():
                self._loop.call_soon_threadsafe(self.server.close)
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None


class PetClient:
    """Client for visiting other pets."""
    
    def __init__(self):
        pass
    
    async def visit_pet(self, host: str, port: int,
                        my_pet_data: dict,
                        timeout: float = 5.0) -> Optional[dict]:
        """Visit a remote pet and exchange data."""
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port), timeout=timeout
            )
            
            # Send our pet data
            writer.write(json.dumps(my_pet_data).encode())
            await writer.drain()
            
            # Receive their pet data
            response = await asyncio.wait_for(reader.read(16384), timeout=timeout)
            
            writer.close()
            await writer.wait_closed()
            
            if response:
                return json.loads(response.decode())
            return None
        except Exception as e:
            return {"error": str(e)}


class DiscoveryService:
    """Discovers other Pet Society instances on the local network."""
    
    def __init__(self, on_discover: Callable[[str, int, str], None]):
        self.on_discover = on_discover  # callback(host, port, pet_name)
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self.discovered: dict = {}  # (host, port) -> pet_name
    
    def _broadcast_listener(self):
        """Listen for discovery broadcasts."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            sock.bind(("", DISCOVERY_MULTICAST_PORT))
            mreq = socket.inet_aton(DISCOVERY_MULTICAST_ADDR) + socket.inet_aton("0.0.0.0")
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except Exception:
            # Fallback: just bind to UDP port without multicast
            pass
        
        sock.settimeout(1.0)
        
        while self.running:
            try:
                data, addr = sock.recvfrom(1024)
                if data == DISCOVERY_MESSAGE:
                    # Someone is looking for pets
                    pass
                elif data.startswith(DISCOVERY_RESPONSE):
                    # Someone responded - parse their info
                    parts = data.decode().split(":")
                    if len(parts) >= 4:
                        host = addr[0]
                        port = int(parts[2])
                        pet_name = parts[3]
                        key = (host, port)
                        if key not in self.discovered:
                            self.discovered[key] = pet_name
                            self.on_discover(host, port, pet_name)
            except socket.timeout:
                continue
            except Exception:
                continue
        
        sock.close()
    
    def _broadcast_sender(self):
        """Periodically send discovery broadcasts."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        
        while self.running:
            try:
                sock.sendto(DISCOVERY_MESSAGE,
                           (DISCOVERY_MULTICAST_ADDR, DISCOVERY_MULTICAST_PORT))
            except Exception:
                pass
            time.sleep(5.0)
        
        sock.close()
    
    def start(self):
        """Start discovery service."""
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._broadcast_listener, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop discovery service."""
        self.running = False
        if self._thread:
            self._thread.join(timeout=1.0)
            self._thread = None


def scan_network(timeout: float = 3.0) -> list:
    """Quick scan of nearby IPs for Pet Society instances."""
    discovered = []
    local_ip = get_local_ip()
    
    if local_ip == "127.0.0.1":
        return discovered
    
    # Try local IP plus a few neighbors
    parts = local_ip.rsplit(".", 1)
    if len(parts) == 2:
        base = parts[0]
        # Scan last octet range around us
        try:
            current = int(parts[1])
            for i in range(max(2, current - 10), min(254, current + 10)):
                host = f"{base}.{i}"
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.3)
                    result = sock.connect_ex((host, DEFAULT_PORT))
                    if result == 0:
                        discovered.append(host)
                    sock.close()
                except Exception:
                    pass
        except ValueError:
            pass
    
    return discovered

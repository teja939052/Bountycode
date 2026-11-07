"""Networks track â€” Computer Networks lessons."""

NETWORKS_LESSONS = [
    {
        "id": "net-intro",
        "title": "Networking Basics",
        "track": "networks",
        "description": "Network types, topologies, OSI model.",
        "difficulty": "beginner",
        "xpReward": 60,
        "steps": [
            {
                "id": "nw1",
                "type": "explain",
                "title": "Network types",
                "content": "LAN (Local Area Network), WAN (Wide Area Network), MAN (Metropolitan Area Network).",
                "code": "",
                "explanation": "LAN covers small area (building), WAN covers large area (country/continent).",
            },
            {
                "id": "nw2",
                "type": "explain",
                "title": "OSI Model",
                "content": "7 layers: Physical, Data Link, Network, Transport, Session, Presentation, Application.",
                "code": "",
                "explanation": "OSI model has 7 layers. Each layer provides services to layer above.",
            },
            {
                "id": "nw3",
                "type": "quiz",
                "title": "OSI layer question",
                "question": "Which layer handles routing?",
                "options": ["Physical", "Data Link", "Network", "Transport"],
                "correctIndex": 2,
                "explanation": "Network layer handles routing and IP addressing.",
            },
        ],
    },
    {
        "id": "net-tcp-ip",
        "title": "TCP/IP Model",
        "track": "networks",
        "description": "TCP/IP model layers and protocols.",
        "difficulty": "beginner",
        "xpReward": 60,
        "steps": [
            {
                "id": "nw4",
                "type": "explain",
                "title": "TCP/IP Model",
                "content": "4 layers: Network Access, Internet, Transport, Application.",
                "code": "",
                "explanation": "TCP/IP is 4-layer model used in Internet.",
            },
            {
                "id": "nw5",
                "type": "explain",
                "title": "TCP vs UDP",
                "content": "TCP is connection-oriented, reliable. UDP is connectionless, unreliable but faster.",
                "code": "",
                "explanation": "TCP guarantees delivery, UDP doesn't guarantee but is faster.",
            },
            {
                "id": "nw6",
                "type": "exercise",
                "title": "Protocol identification",
                "instruction": "Which protocol uses port 80?",
                "starterCode": "",
                "solution": "HTTP uses port 80.",
                "tests": [{"input": None, "expected": None, "check": "equals_80"}],
                "explanation": "HTTP uses port 80, HTTPS uses 443, FTP uses 21, SSH uses 22.",
            },
        ],
    },
    {
        "id": "networks-protocols",
        "title": "Common Protocols",
        "track": "networks",
        "description": "HTTP, FTP, SMTP, DNS, DHCP.",
        "difficulty": "beginner",
        "xpReward": 60,
        "steps": [
            {
                "id": "nw7",
                "type": "explain",
                "title": "Common protocols",
                "content": "HTTP (web), FTP (file transfer), SMTP (email send), POP3/IMAP (email receive), DNS (domain name resolution), DHCP (IP assignment).",
                "code": "",
                "explanation": "Each protocol serves specific purpose in networking.",
            },
            {
                "id": "nw8",
                "type": "quiz",
                "title": "Protocol question",
                "question": "Which protocol resolves domain names to IP addresses?",
                "options": ["HTTP", "DNS", "SMTP", "DHCP"],
                "correctIndex": 1,
                "explanation": "DNS (Domain Name System) resolves domain names to IP addresses.",
            },
        ],
    },
    {
        "id": "net-osi",
        "title": "OSI Model",
        "description": "Seven layers of networking.",
        "track": "networks",
        "difficulty": "beginner",
        "xpReward": 60,
        "steps": [
            {
                "id": "osi1",
                "type": "explain",
                "title": "Seven layers",
                "content": "OSI model: Physical, Data Link, Network, Transport, Session, Presentation, Application. Each layer serves the one above and is served by the one below.",
                "code": "",
                "explanation": "Mnemonic: 'Please Do Not Throw Sausage Pizza Away' (Physical to Application).",
            },
            {
                "id": "osi2",
                "type": "exercise",
                "title": "Layer identification",
                "instruction": "HTTP operates at which OSI layer?",
                "starterCode": "",
                "solution": "Application layer (Layer 7). HTTP is the protocol for web browsing, used by applications.",
                "tests": [{"input": None, "expected": None, "check": "equals_application"}],
                "explanation": "HTTP is an application-layer protocol (Layer 7).",
            },
            {
                "id": "osi3",
                "type": "quiz",
                "title": "Layer functions",
                "question": "Which OSI layer handles end-to-end error recovery and flow control?",
                "options": ["Data Link", "Network", "Transport", "Application"],
                "correctIndex": 2,
                "explanation": "Transport layer (Layer 4) provides end-to-end communication, error recovery, and flow control (e.g., TCP).",
            },
        ],
    },
    {
        "id": "net-http",
        "title": "HTTP and Web",
        "description": "HTTP protocol, status codes, REST basics.",
        "track": "networks",
        "difficulty": "beginner",
        "xpReward": 60,
        "steps": [
            {
                "id": "http1",
                "type": "explain",
                "title": "HTTP basics",
                "content": "HTTP is a request-response protocol. Client sends request (GET, POST, PUT, DELETE), server responds with status code and body. Stateless: each request independent.",
                "code": "",
                "explanation": "Common methods: GET (retrieve), POST (create), PUT (update), DELETE (remove).",
            },
            {
                "id": "http2",
                "type": "exercise",
                "title": "Status codes",
                "instruction": "What does HTTP 404 mean?",
                "starterCode": "",
                "solution": "404 Not Found - the server cannot find the requested resource.",
                "tests": [{"input": None, "expected": None, "check": "equals_not_found"}],
                "explanation": "4xx codes are client errors. 404 specifically means resource not found.",
            },
            {
                "id": "http3",
                "type": "quiz",
                "title": "HTTP methods",
                "question": "Which HTTP method is idempotent and used to update a resource?",
                "options": ["POST", "PUT", "DELETE", "PATCH"],
                "correctIndex": 1,
                "explanation": "PUT is idempotent (same request multiple times = same result) and replaces/updates a resource.",
            },
        ],
    },
    {
        "id": "net-ip-addressing-subnetting",
        "title": "IP Addressing and Subnetting",
        "track": "networks",
        "description": "Understand IPv4 addresses, network prefixes, and subnet masks.",
        "difficulty": "intermediate",
        "prerequisites": ["net-tcp-ip"],
        "xpReward": 95,
        "steps": [
            {
                "id": "nip1",
                "type": "explain",
                "title": "Network and host portions",
                "content": "An IPv4 address contains 32 bits. A prefix length such as /24 tells how many leading bits identify the network; the remaining bits identify addresses within that subnet. The subnet mask is another way to represent the prefix.",
                "code": "Address: 192.168.1.10/24\nNetwork: 192.168.1.0\nHost portion: final 8 bits",
                "output": "The /24 prefix corresponds to mask 255.255.255.0",
                "explanation": "Twenty-four bits are network bits and eight bits remain for the host portion."
            },
            {
                "id": "nip2",
                "type": "explain",
                "title": "Calculate a simple subnet",
                "content": "For a /24 IPv4 subnet, the first 24 bits are fixed as the network prefix. The final 8 bits vary across addresses. In a traditional subnet, the all-zero host address identifies the network and the all-one host address is the broadcast address; special-purpose ranges and modern subnet sizes have exceptions.",
                "code": "192.168.1.0/24\nNetwork address: 192.168.1.0\nBroadcast address: 192.168.1.255\nTraditional usable host range: 192.168.1.1–192.168.1.254",
                "output": "254 traditional usable host addresses",
                "explanation": "A /24 contains 256 total addresses; subtract network and broadcast addresses for 254 traditional host addresses."
            },
            {
                "id": "nip3",
                "type": "exercise",
                "title": "Read a CIDR prefix",
                "instruction": "For IPv4 address 10.0.0.5/8, state the subnet mask and network address.",
                "starterCode": "Prefix length: 8\nSubnet mask: ?\nNetwork address: ?",
                "solution": "Subnet mask: 255.0.0.0\nNetwork address: 10.0.0.0",
                "tests": [{"input": null, "expected": "255.0.0.0 and 10.0.0.0", "check": "identifies_slash_8_network"}],
                "explanation": "A /8 prefix fixes the first octet as the network portion."
            },
            {
                "id": "nip4",
                "type": "quiz",
                "title": "Interpret CIDR",
                "question": "How many bits are used for the network prefix in 172.16.0.0/16?",
                "options": ["8", "16", "24", "32"],
                "correctIndex": 1,
                "explanation": "The number after the slash is the prefix length in bits."
            }
        ]
    },
    {
        "id": "net-dns-tls",
        "title": "DNS, HTTPS and TLS",
        "track": "networks",
        "description": "Understand name resolution and how TLS protects web connections.",
        "difficulty": "intermediate",
        "prerequisites": ["net-http"],
        "xpReward": 100,
        "steps": [
            {
                "id": "nd1",
                "type": "explain",
                "title": "What DNS does",
                "content": "The Domain Name System (DNS) maps domain names to records such as IP addresses. A client may use a resolver, which can query DNS servers and cache answers for their time-to-live (TTL). DNS helps people use memorable names instead of remembering numeric addresses.",
                "code": "example.com → DNS lookup → IP address",
                "output": "The client receives an address record such as an IPv4 A record or IPv6 AAAA record",
                "explanation": "DNS resolution happens before a client can connect to the resolved server address."
            },
            {
                "id": "nd2",
                "type": "explain",
                "title": "How HTTPS uses TLS",
                "content": "HTTPS is HTTP carried over a TLS-protected connection. TLS helps provide confidentiality and integrity, and it authenticates the server using certificates. Certificate validation checks that the certificate is trusted and matches the requested hostname.",
                "code": "Browser → TLS handshake and certificate validation → encrypted HTTP requests",
                "output": "HTTP messages are carried inside the protected TLS connection",
                "explanation": "TLS protects data in transit; it does not by itself guarantee that a website or its content is trustworthy."
            },
            {
                "id": "nd3",
                "type": "explain",
                "title": "Understand the handshake at a high level",
                "content": "During a TLS handshake, the client and server negotiate supported cryptographic parameters, authenticate the server, and establish shared session keys. Modern TLS versions use ephemeral key agreement to establish keys without sending the session secret directly.",
                "code": "ClientHello → ServerHello and certificate → key agreement → protected application data",
                "output": "The peers establish keys for the secure session",
                "explanation": "This is a simplified conceptual flow; exact handshake messages differ by TLS version and configuration."
            },
            {
                "id": "nd4",
                "type": "quiz",
                "title": "Identify DNS",
                "question": "Which service translates a domain name into IP address records?",
                "options": ["DNS", "DHCP", "NAT", "FTP"],
                "correctIndex": 0,
                "explanation": "DNS resolves names to resource records, commonly including IP addresses."
            }
        ]
    },
    {
        "id": "net-tcp-udp-handshake",
        "title": "TCP, UDP and Reliable Delivery",
        "track": "networks",
        "description": "Compare transport protocols and understand the TCP connection handshake.",
        "difficulty": "intermediate",
        "prerequisites": ["net-tcp-ip"],
        "xpReward": 95,
        "steps": [
            {
                "id": "ntu1",
                "type": "explain",
                "title": "Compare TCP and UDP",
                "content": "TCP provides a reliable, ordered byte stream with connection management, retransmission, and flow control. UDP sends independent datagrams without TCP's built-in delivery and ordering guarantees. Applications choose based on their latency, reliability, and message requirements.",
                "code": "TCP: connection-oriented byte stream\nUDP: connectionless datagrams",
                "output": "",
                "explanation": "Neither protocol is universally better; the application requirements determine the choice."
            },
            {
                "id": "ntu2",
                "type": "explain",
                "title": "TCP three-way handshake",
                "content": "TCP establishes a connection using a three-way handshake: the client sends SYN, the server replies SYN-ACK, and the client sends ACK. This synchronizes initial sequence numbers and confirms that both sides can communicate.",
                "code": "Client → SYN → Server\nClient ← SYN-ACK ← Server\nClient → ACK → Server",
                "output": "Connection established",
                "explanation": "The three messages establish the initial TCP connection state."
            },
            {
                "id": "ntu3",
                "type": "explain",
                "title": "Flow control and congestion control",
                "content": "Flow control protects a receiver from being overwhelmed; TCP advertises a receive window. Congestion control responds to network conditions to reduce the risk of overloading the network. They solve related but different problems.",
                "code": "Receiver capacity → receive window\nNetwork capacity → congestion window",
                "output": "",
                "explanation": "The sender's usable in-flight data is constrained by both receiver flow control and congestion control."
            },
            {
                "id": "ntu4",
                "type": "quiz",
                "title": "Choose UDP",
                "question": "Which transport protocol sends datagrams without TCP's built-in reliable ordered byte-stream guarantee?",
                "options": ["TCP", "UDP", "HTTP", "TLS"],
                "correctIndex": 1,
                "explanation": "UDP is a datagram transport and does not provide TCP-style reliability and ordering."
            }
        ]
    }
]

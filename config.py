PORT_SECURITY_DB = {
    21: {
        "service": "FTP",
        "risk": "HIGH",
        "detail": "Unencrypted File Transfer - Risk of Credential Theft",
    },
    22: {
        "service": "SSH",
        "risk": "LOW",
        "detail": "Encrypted Administrative Remote Shell",
    },
    53: {
        "service": "DNS",
        "risk": "MEDIUM",
        "detail": "Core Resolution Pipeline - Verify Recursion Settings",
    },
    80: {
        "service": "HTTP",
        "risk": "HIGH",
        "detail": "Cleartext Web Traffic - Recommend Enforcing HTTPS (443)",
    },
    443: {
        "service": "HTTPS",
        "risk": "LOW",
        "detail": "Encrypted Secure Web Service",
    },
    3389: {
        "service": "RDP",
        "risk": "CRITICAL",
        "detail": "Exposed Remote Desktop Endpoint - Target for Brute-force",
    },
}

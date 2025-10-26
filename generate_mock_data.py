import pandas as pd
import json

# Mock IT Knowledge Base Data
it_knowledge_base = [
    {
        "id": "KB001",
        "category": "Password Reset",
        "title": "How to Reset Your Password",
        "content": """To reset your company password:
1. Go to https://password.company.com
2. Click 'Forgot Password'
3. Enter your employee ID and registered email
4. Check your email for reset link (valid for 24 hours)
5. Create a new password following policy: minimum 12 characters, uppercase, lowercase, number, and special character
6. Login with new credentials
If you don't receive the email within 15 minutes, contact IT support.""",
        "tags": ["password", "reset", "login", "access"],
        "related_issues": ["account_locked", "email_access"]
    },
    {
        "id": "KB002",
        "category": "VPN Setup",
        "title": "VPN Connection Setup Guide",
        "content": """Setting up company VPN:
1. Download Cisco AnyConnect from company portal
2. Install the application (requires admin rights)
3. Launch Cisco AnyConnect
4. Enter VPN address: vpn.company.com
5. Use your network credentials (same as Windows login)
6. Accept the security certificate
7. You're connected when you see the green checkmark
Troubleshooting: If connection fails, ensure your antivirus allows VPN traffic. Check firewall settings.""",
        "tags": ["vpn", "remote", "connection", "cisco", "anyconnect"],
        "related_issues": ["remote_access", "network_issues"]
    },
    {
        "id": "KB003",
        "category": "Software Installation",
        "title": "Installing Microsoft Office 365",
        "content": """To install Office 365:
1. Login to https://portal.office.com with company email
2. Click 'Install Office' button (top right)
3. Select 'Office 365 apps'
4. Download and run the installer
5. Sign in with your company email when prompted
6. Office apps will install automatically (Word, Excel, PowerPoint, Outlook, Teams)
7. Restart your computer after installation
License: Your account includes 5 device installations. Deactivate unused devices from portal.""",
        "tags": ["office", "microsoft", "software", "installation", "365"],
        "related_issues": ["software_license", "activation"]
    },
    {
        "id": "KB004",
        "category": "Email Issues",
        "title": "Outlook Email Not Syncing",
        "content": """If Outlook isn't syncing:
1. Check internet connection
2. Verify you're connected to VPN (if remote)
3. Click Send/Receive All Folders button
4. Clear Outlook cache: File > Options > Advanced > Outlook Data File Settings
5. Restart Outlook in safe mode: Hold Ctrl while launching
6. Repair Outlook data file: Control Panel > Mail > Data Files > Settings > Compact Now
7. Recreate Outlook profile if issue persists
Check mailbox size: Limit is 50GB. Archive old emails if near limit.""",
        "tags": ["outlook", "email", "sync", "mail", "not working"],
        "related_issues": ["email_not_received", "slow_outlook"]
    },
    {
        "id": "KB005",
        "category": "Hardware Issues",
        "title": "Printer Not Responding",
        "content": """Troubleshooting printer issues:
1. Check printer power and cable connections
2. Verify printer shows as 'Ready' on display
3. On computer: Control Panel > Devices and Printers
4. Right-click printer > Set as default printer
5. Right-click printer > See what's printing > Cancel all documents
6. Restart Print Spooler service: Services.msc > Print Spooler > Restart
7. Update printer driver from manufacturer website
8. For network printers, verify network connection and IP address
Common issue: Printer offline mode. Right-click printer > uncheck 'Use Printer Offline'.""",
        "tags": ["printer", "printing", "hardware", "not responding", "offline"],
        "related_issues": ["print_queue", "driver_issue"]
    },
    {
        "id": "KB006",
        "category": "Access Request",
        "title": "Requesting Access to Shared Drives",
        "content": """To request access to shared network drives:
1. Open ServiceNow portal: https://service.company.com
2. Click 'Request Access'
3. Select 'Network Drive Access'
4. Enter drive path (e.g., \\\\fileserver\\department)
5. Specify access level needed: Read or Read/Write
6. Provide business justification
7. Select your manager for approval
8. Submit request (typical approval time: 2-4 hours)
Access is automatically granted after manager approval. You'll receive email notification.""",
        "tags": ["access", "permissions", "shared drive", "folder", "network"],
        "related_issues": ["permission_denied", "folder_access"]
    },
    {
        "id": "KB007",
        "category": "Software Issues",
        "title": "Application Freezing or Crashing",
        "content": """When applications freeze or crash:
1. Wait 30 seconds - application may be processing
2. Check Task Manager (Ctrl+Shift+Esc) for CPU/memory usage
3. End unresponsive application: Task Manager > select app > End Task
4. Clear application cache and temp files
5. Update application to latest version
6. Check available disk space (need at least 20GB free)
7. Scan for malware using company antivirus
8. Check Windows Event Viewer for error logs
If problem persists with specific application, create IT ticket with error screenshots.""",
        "tags": ["application", "crash", "freeze", "not responding", "software"],
        "related_issues": ["slow_computer", "performance"]
    },
    {
        "id": "KB008",
        "category": "Account Issues",
        "title": "Account Locked Out",
        "content": """If your account is locked:
1. Account locks after 5 failed login attempts
2. Automatic unlock occurs after 30 minutes
3. For immediate unlock: Call IT Help Desk at ext. 4357
4. Verify you're using correct password (check Caps Lock)
5. Password expires every 90 days - reset if needed
6. If repeatedly locking, your password may be compromised
Prevention: Never share passwords, use password manager, enable MFA (multi-factor authentication).""",
        "tags": ["locked", "account", "login", "lockout", "access denied"],
        "related_issues": ["password_reset", "cannot_login"]
    },
    {
        "id": "KB009",
        "category": "Network Issues",
        "title": "No Internet Connection",
        "content": """Troubleshooting internet connectivity:
1. Check physical connections: ethernet cable or WiFi
2. For WiFi: Ensure connected to company network (CompanyWiFi)
3. Restart network adapter: Network Settings > Change adapter options > Disable/Enable
4. Release and renew IP: Command Prompt (Admin) > ipconfig /release then ipconfig /renew
5. Flush DNS: ipconfig /flushdns
6. Check proxy settings: Internet Options > Connections > LAN settings
7. Temporarily disable antivirus/firewall to test
8. Restart computer
For company WiFi password: Contact IT Help Desk (changes quarterly).""",
        "tags": ["internet", "network", "connection", "wifi", "connectivity"],
        "related_issues": ["vpn_issues", "slow_internet"]
    },
    {
        "id": "KB010",
        "category": "Mobile Device",
        "title": "Setting Up Company Email on Mobile",
        "content": """Configure company email on smartphone:
For iPhone:
1. Settings > Mail > Accounts > Add Account > Exchange
2. Email: your.email@company.com
3. Server: outlook.office365.com
4. Domain: leave blank
5. Username: your.email@company.com
6. Password: your company password
7. Enable Mail, Contacts, Calendars

For Android:
1. Settings > Accounts > Add Account > Exchange
2. Enter email and password
3. Server: outlook.office365.com
4. Domain\\Username: company\\your.email
5. Complete setup

MFA may require Microsoft Authenticator app approval.""",
        "tags": ["mobile", "phone", "email", "iphone", "android", "setup"],
        "related_issues": ["mobile_access", "email_sync"]
    },
    {
        "id": "KB011",
        "category": "Security",
        "title": "Reporting Phishing or Suspicious Emails",
        "content": """If you receive suspicious email:
DO NOT:
- Click any links
- Download attachments
- Reply to sender
- Provide personal information

DO:
1. In Outlook, select the email
2. Click Report Message button (top ribbon)
3. Select 'Phishing'
4. Email forwards to security team automatically
5. Delete email from inbox

Warning signs of phishing:
- Urgent requests for action
- Requests for password/personal info
- Suspicious sender address
- Poor grammar/spelling
- Unexpected attachments
- Mismatched URLs (hover to check)

Security team reviews within 1 hour. Stay vigilant!""",
        "tags": ["phishing", "security", "suspicious", "email", "spam", "scam"],
        "related_issues": ["security_incident", "compromised_account"]
    },
    {
        "id": "KB012",
        "category": "Teams",
        "title": "Microsoft Teams Audio/Video Issues",
        "content": """Troubleshooting Teams meeting problems:
Audio issues:
1. Click profile picture > Settings > Devices
2. Test audio device and speaker
3. Ensure correct microphone selected
4. Check microphone isn't muted (hardware switch)
5. Grant Teams microphone permissions (Windows Settings > Privacy)

Video issues:
1. Verify camera isn't used by another app
2. Check camera privacy settings
3. Update camera driver
4. Restart Teams completely (not just close)

Poor quality:
1. Close unnecessary applications
2. Use wired connection instead of WiFi
3. Reduce video quality: Settings > Call quality
4. Check bandwidth: need 1.5 Mbps for video calls""",
        "tags": ["teams", "meeting", "audio", "video", "camera", "microphone"],
        "related_issues": ["video_conferencing", "call_quality"]
    },
    {
        "id": "KB013",
        "category": "Data Backup",
        "title": "How to Backup Your Work Files",
        "content": """Company backup options:
OneDrive (Recommended):
1. Save files to OneDrive folder (auto-syncs)
2. Files accessible from any device
3. 1TB storage per user
4. Automatic versioning (restore previous versions)

Network Drives:
1. Save to department shared drives
2. IT performs nightly backups
3. File recovery available up to 30 days

DO NOT store critical files only on local C: drive
Backup frequency: OneDrive syncs continuously, Network drives backed up daily at midnight

To restore deleted files:
OneDrive: Check Recycle Bin (90 day retention)
Network: Submit IT ticket with file path and date needed""",
        "tags": ["backup", "onedrive", "files", "recovery", "storage"],
        "related_issues": ["file_recovery", "deleted_files"]
    },
    {
        "id": "KB014",
        "category": "Performance",
        "title": "Computer Running Slow",
        "content": """Speed up slow computer:
Immediate actions:
1. Close unnecessary programs and browser tabs
2. Restart computer (if not done in 7+ days)
3. Check Task Manager for resource-hungry processes
4. Disconnect external drives

Maintenance:
1. Run Disk Cleanup: Search > Disk Cleanup
2. Empty Recycle Bin
3. Clear browser cache
4. Uninstall unused programs
5. Disable startup programs: Task Manager > Startup tab
6. Check disk space: Need 20GB+ free
7. Run Windows Update
8. Perform malware scan
9. Defragment hard drive (if using HDD, not SSD)

If still slow after all steps, may need hardware upgrade. Contact IT for evaluation.""",
        "tags": ["slow", "performance", "speed", "computer", "lag"],
        "related_issues": ["application_crash", "freeze"]
    },
    {
        "id": "KB015",
        "category": "System Access",
        "title": "Multi-Factor Authentication (MFA) Setup",
        "content": """Setting up MFA for enhanced security:
1. Install Microsoft Authenticator on smartphone
2. Login to https://aka.ms/mfasetup
3. Click 'Set up Authenticator app'
4. Scan QR code with Authenticator app
5. Enter 6-digit code shown in app
6. Complete setup

Using MFA:
- Login with username/password
- Approve notification on phone OR enter code from app
- Option to trust device for 30 days

Lost phone?
- Use backup codes (provided during setup)
- Call IT Help Desk for emergency access
- Update phone number: https://aka.ms/mfasetup

MFA is mandatory for all employees for security compliance.""",
        "tags": ["mfa", "authentication", "security", "2fa", "two-factor"],
        "related_issues": ["login_issues", "security_setup"]
    }
]

# Create DataFrame
df = pd.DataFrame(it_knowledge_base)

# Save to JSON
with open('it_knowledge_base.json', 'w', encoding='utf-8') as f:
    json.dump(it_knowledge_base, f, indent=2, ensure_ascii=False)

# Save to CSV
df.to_csv('it_knowledge_base.csv', index=False, encoding='utf-8')

print(f"Created knowledge base with {len(it_knowledge_base)} articles")
print(f"\nCategories: {df['category'].unique().tolist()}")
print(f"\nFiles created:")
print("- it_knowledge_base.json")
print("- it_knowledge_base.csv")

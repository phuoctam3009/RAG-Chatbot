"""
Function calling definitions for IT Support Chatbot
These functions extend the chatbot's capabilities beyond knowledge retrieval
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
import random

# Simulated ticket system
TICKET_DATABASE = []
TICKET_COUNTER = 1000

def create_support_ticket(
    title: str,
    description: str,
    category: str,
    priority: str = "medium"
) -> Dict:
    """
    Create a new IT support ticket
    
    Args:
        title: Brief title of the issue
        description: Detailed description of the problem
        category: Issue category (password, hardware, software, network, access, other)
        priority: Ticket priority (low, medium, high, critical)
    
    Returns:
        Dictionary with ticket details
    """
    global TICKET_COUNTER
    
    ticket = {
        "ticket_id": f"INC{TICKET_COUNTER}",
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "status": "open",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estimated_resolution": get_resolution_time(priority),
        "assigned_to": "IT Support Team"
    }
    
    TICKET_DATABASE.append(ticket)
    TICKET_COUNTER += 1
    
    return ticket

def check_ticket_status(ticket_id: str) -> Dict:
    """
    Check the status of an existing support ticket
    
    Args:
        ticket_id: The ticket ID (e.g., INC1000)
    
    Returns:
        Dictionary with ticket status information
    """
    for ticket in TICKET_DATABASE:
        if ticket["ticket_id"] == ticket_id:
            return {
                "found": True,
                "ticket_id": ticket["ticket_id"],
                "status": ticket["status"],
                "title": ticket["title"],
                "priority": ticket["priority"],
                "created_at": ticket["created_at"],
                "estimated_resolution": ticket["estimated_resolution"]
            }
    
    return {
        "found": False,
        "message": f"Ticket {ticket_id} not found in the system"
    }

def check_system_status(system_name: str) -> Dict:
    """
    Check the operational status of company systems
    
    Args:
        system_name: Name of the system to check (email, vpn, file_server, internet, office365)
    
    Returns:
        Dictionary with system status information
    """
    # Simulated system status
    systems = {
        "email": {"status": "operational", "uptime": "99.9%", "last_incident": "2 days ago"},
        "vpn": {"status": "operational", "uptime": "99.5%", "last_incident": "5 days ago"},
        "file_server": {"status": "operational", "uptime": "99.8%", "last_incident": "1 day ago"},
        "internet": {"status": "operational", "uptime": "99.95%", "last_incident": "10 days ago"},
        "office365": {"status": "operational", "uptime": "99.9%", "last_incident": "3 days ago"},
        "printer": {"status": "degraded", "uptime": "95%", "last_incident": "2 hours ago", 
                   "note": "Building B printers experiencing delays"},
    }
    
    system_name = system_name.lower().replace(" ", "_")
    
    if system_name in systems:
        return {
            "system": system_name,
            **systems[system_name]
        }
    else:
        return {
            "system": system_name,
            "status": "unknown",
            "message": "System not monitored or invalid system name"
        }

def search_employee_directory(name: str = None, department: str = None, email: str = None) -> List[Dict]:
    """
    Search the employee directory
    
    Args:
        name: Employee name to search
        department: Department to filter by
        email: Email address to search
    
    Returns:
        List of matching employee records
    """
    # Mock employee directory
    employees = [
        {"name": "John Smith", "email": "john.smith@company.com", "department": "IT Support", 
         "phone": "ext. 4357", "location": "Building A, Floor 3"},
        {"name": "Sarah Johnson", "email": "sarah.johnson@company.com", "department": "IT Security", 
         "phone": "ext. 4358", "location": "Building A, Floor 3"},
        {"name": "Mike Chen", "email": "mike.chen@company.com", "department": "Network Admin", 
         "phone": "ext. 4359", "location": "Building A, Floor 3"},
        {"name": "Emily Davis", "email": "emily.davis@company.com", "department": "IT Manager", 
         "phone": "ext. 4350", "location": "Building A, Floor 3"},
    ]
    
    results = employees
    
    if name:
        results = [e for e in results if name.lower() in e["name"].lower()]
    if department:
        results = [e for e in results if department.lower() in e["department"].lower()]
    if email:
        results = [e for e in results if email.lower() in e["email"].lower()]
    
    return results

def get_resolution_time(priority: str) -> str:
    """Helper function to determine estimated resolution time"""
    times = {
        "low": "3-5 business days",
        "medium": "1-2 business days",
        "high": "4-8 hours",
        "critical": "1-2 hours"
    }
    return times.get(priority.lower(), "2-3 business days")

def schedule_maintenance(system: str, date: str, duration: str) -> Dict:
    """
    Schedule maintenance window for a system (Admin function)
    
    Args:
        system: System name
        date: Maintenance date
        duration: Expected duration
    
    Returns:
        Maintenance schedule confirmation
    """
    return {
        "scheduled": True,
        "system": system,
        "date": date,
        "duration": duration,
        "notification": "Users will be notified 24 hours in advance",
        "maintenance_id": f"MAINT{random.randint(1000, 9999)}"
    }

# Function definitions for OpenAI function calling
FUNCTION_DEFINITIONS = [
    {
        "name": "create_support_ticket",
        "description": "Create a new IT support ticket when the user's issue cannot be resolved through the knowledge base or when they explicitly request to create a ticket",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Brief title summarizing the issue (max 100 characters)"
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the problem including what the user has already tried"
                },
                "category": {
                    "type": "string",
                    "enum": ["password", "hardware", "software", "network", "access", "other"],
                    "description": "Category of the IT issue"
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "critical"],
                    "description": "Priority level: critical (system down), high (affecting work), medium (inconvenient), low (minor)"
                }
            },
            "required": ["title", "description", "category"]
        }
    },
    {
        "name": "check_ticket_status",
        "description": "Check the current status of an existing IT support ticket using the ticket ID",
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "string",
                    "description": "The ticket ID (format: INC followed by numbers, e.g., INC1000)"
                }
            },
            "required": ["ticket_id"]
        }
    },
    {
        "name": "check_system_status",
        "description": "Check if a company system or service is currently operational",
        "parameters": {
            "type": "object",
            "properties": {
                "system_name": {
                    "type": "string",
                    "enum": ["email", "vpn", "file_server", "internet", "office365", "printer"],
                    "description": "Name of the system to check status"
                }
            },
            "required": ["system_name"]
        }
    },
    {
        "name": "search_employee_directory",
        "description": "Search for employee contact information in the company directory",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Employee name to search for"
                },
                "department": {
                    "type": "string",
                    "description": "Department name to filter results"
                },
                "email": {
                    "type": "string",
                    "description": "Email address to search for"
                }
            }
        }
    }
]

# Map function names to actual functions
AVAILABLE_FUNCTIONS = {
    "create_support_ticket": create_support_ticket,
    "check_ticket_status": check_ticket_status,
    "check_system_status": check_system_status,
    "search_employee_directory": search_employee_directory
}

def execute_function(function_name: str, arguments: Dict) -> str:
    """
    Execute a function and return the result as a JSON string
    
    Args:
        function_name: Name of the function to execute
        arguments: Dictionary of arguments to pass to the function
    
    Returns:
        JSON string with the function result
    """
    if function_name in AVAILABLE_FUNCTIONS:
        function = AVAILABLE_FUNCTIONS[function_name]
        result = function(**arguments)
        return json.dumps(result, indent=2)
    else:
        return json.dumps({"error": f"Function {function_name} not found"})

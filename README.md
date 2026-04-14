## DeployHub - Integration & CI/CD Project ##

### IS2209 Group Project

University College Cork 

**- Team:** Group 23

**- Team Members:**
- Daniel O'Conor - 124465772
- Mark O'Sullivan - 124369726
- Kevin Murphy - 124486342
- Ted McGrath - 124482326


## Links
- **GitHub Repository:** https://github.com/Danieloc06/Tutorial2
- **Application:** http://127.0.0.1:5000/
- **Microsoft Planner:** https://planner.cloud.microsoft/webui/plan/gFNTTN5sYEym-QVFN-vAcpYABSQ5/view/board?tid=46fe5ca5-866f-4e42-92e9-ed8786245545
- **Live Application:** https://is2209-web-service.onrender.com/

## API Key
API_KEY = 3682f760

## Databse URL
DATABASE_URL=postgresql://postgres.yxfoxuflewgvewyhglgr:Supabasepass123@aws-1-eu-west-1.pooler.supabase.com:5432/postgres

## Secret Key
SECRET_KEY="dnfisjognjs"
### System Description

DeployHub is a small integration-focused web service 
built using Flask that aggregates data from multiple
sources and exposes a consolidated API and optional
web interface.

## Technology Stack

- **Backend**: Python 3.11+, Flask
- **Database**: Supabase
- **Frontend**: HTML
- **External API**: Movie API
- **Testing**: pytest

### Steps
1. **Run the application**

   - Run app.py

2. **Access the application**
   - Open your browser and navigate to: http://127.0.0.1:5000

## API Endpoints
- Endpoint: /         -        Search Movie: http://127.0.0.1:5000/index/
- Endpoint: /view/    -        View Entry of Movies: http://127.0.0.1:5000/view/
- Endpoint: /status   -       View Database Status: http://127.0.0.1:5000/status
- Endpoint: /ready    -        View Database Readiness: http://127.0.0.1:5000/ready

## Run tests:

- run tests/test_app_works.py
- run tests/test_app_works_correctly.py 
- run tests/test_search.py 


## Tests
- **test_app_works.py**: 6 tests 
- **test_app_works_correctly.py**: 2 tests
- **test_search.py**: 2 tests

## References 
- Geeks for geeks
- Stack Overflow


## Additional Information
- **Submitted for Assessment**: IS2209 Module
- **Submission Date**: 14th April 2026

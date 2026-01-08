# Vercel entry point
# Vercel will use this file when requests come to /
# This wraps the FastAPI app with Mangum to make it compatible with Vercel's serverless functions

from mangum import Mangum
import sys
import os

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import the FastAPI app
from server import app

# Wrap FastAPI app with Mangum for AWS Lambda/Vercel compatibility
# Mangum converts ASGI (FastAPI) to Lambda handler format
handler = Mangum(app, lifespan="off")

# Export handler for Vercel
# Vercel looks for 'handler' or 'app' in serverless functions
__all__ = ['handler', 'app']


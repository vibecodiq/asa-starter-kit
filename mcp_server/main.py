"""
MCP Server - Main Application

FastAPI server for slice generation.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from .handlers import generate_spec, generate_contract, generate_skeleton

app = FastAPI(
    title="ASA MCP Server",
    description="Model Context Protocol server for ASA slice generation",
    version="0.9.0"
)


class GenerateSpecRequest(BaseModel):
    func_spec: str
    domain: str
    slice_name: str


class GenerateContractRequest(BaseModel):
    spec_md: str
    domain: str
    slice_name: str


class GenerateSkeletonRequest(BaseModel):
    func_spec: str
    domain: str
    slice_name: str
    output_path: str


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "service": "ASA MCP Server",
        "version": "0.9.0"
    }


@app.post("/mcp/generate-spec")
async def generate_spec_endpoint(request: GenerateSpecRequest):
    """
    Generate slice.spec.md from functional specification.

    Returns:
        spec_md: Generated spec.md content
    """
    try:
        spec_md = generate_spec.generate(
            func_spec=request.func_spec,
            domain=request.domain,
            slice_name=request.slice_name
        )
        return {
            "spec_md": spec_md,
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mcp/generate-contract")
async def generate_contract_endpoint(request: GenerateContractRequest):
    """
    Generate slice.contract.json from spec.md.

    Returns:
        contract_json: Generated contract.json content
    """
    try:
        contract_json = generate_contract.generate(
            spec_md=request.spec_md,
            domain=request.domain,
            slice_name=request.slice_name
        )
        return {
            "contract_json": contract_json,
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mcp/generate-skeleton")
async def generate_skeleton_endpoint(request: GenerateSkeletonRequest):
    """
    Generate complete slice skeleton (all files).

    Returns:
        created_files: List of created file paths
    """
    try:
        created_files = generate_skeleton.generate(
            func_spec=request.func_spec,
            domain=request.domain,
            slice_name=request.slice_name,
            output_path=Path(request.output_path)
        )
        return {
            "created_files": created_files,
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    import sys

    port = 8001
    if "--port" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1])

    print(f"Starting MCP Server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)

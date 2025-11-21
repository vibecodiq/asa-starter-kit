"""Generate slice.contract.json"""
import json
from jinja2 import Template
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "slice.contract.json.j2"

def to_camel_case(snake_str: str) -> str:
    """Convert snake_case to CamelCase"""
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)

def generate(spec_md: str, domain: str, slice_name: str) -> str:
    """
    Generate slice.contract.json from spec.md.

    Args:
        spec_md: Slice specification markdown
        domain: Domain name
        slice_name: Slice name

    Returns:
        Generated contract.json content (JSON string)
    """
    # Load template
    with open(TEMPLATE_PATH, "r") as f:
        template_str = f.read()
    
    # Create template with custom filter
    from jinja2 import Environment
    env = Environment()
    env.filters['to_camel_case'] = to_camel_case
    template = env.from_string(template_str)

    # Extract info from spec (simple parsing)

    # Render template
    contract_json = template.render(
        domain=domain,
        slice_name=slice_name,
        full_slice_name=f"{domain}/{slice_name}"
    )

    # Validate JSON
    json.loads(contract_json)  # Will raise if invalid

    return contract_json

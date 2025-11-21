"""Generate slice.spec.md"""
from jinja2 import Template
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "slice.spec.md.j2"

def to_camel_case(snake_str: str) -> str:
    """Convert snake_case to CamelCase"""
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)

def generate(func_spec: str, domain: str, slice_name: str) -> str:
    """
    Generate slice.spec.md from functional specification.

    Args:
        func_spec: Functional specification (plain text)
        domain: Domain name
        slice_name: Slice name

    Returns:
        Generated spec.md content
    """
    # Load template
    with open(TEMPLATE_PATH, "r") as f:
        template_str = f.read()
    
    # Create template with custom filter
    from jinja2 import Environment
    env = Environment()
    env.filters['to_camel_case'] = to_camel_case
    template = env.from_string(template_str)

    # Parse func_spec (simple extraction)
    goal = func_spec[:200] if len(func_spec) > 200 else func_spec

    # Render template
    spec_md = template.render(
        domain=domain,
        slice_name=slice_name,
        goal=goal,
        func_spec=func_spec
    )

    return spec_md

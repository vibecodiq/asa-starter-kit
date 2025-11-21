"""Generate complete slice skeleton"""
from pathlib import Path
from jinja2 import Template
from . import generate_spec, generate_contract

def to_camel_case(snake_str: str) -> str:
    """Convert snake_case to CamelCase"""
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)

def generate(func_spec: str, domain: str, slice_name: str, output_path: Path) -> list[str]:
    """
    Generate complete slice skeleton.

    Args:
        func_spec: Functional specification
        domain: Domain name
        slice_name: Slice name
        output_path: Output directory path

    Returns:
        List of created file paths
    """
    created_files = []

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate spec.md
    spec_md = generate_spec.generate(func_spec, domain, slice_name)
    spec_path = output_path / "slice.spec.md"
    spec_path.write_text(spec_md)
    created_files.append(str(spec_path))

    # Generate contract.json
    contract_json = generate_contract.generate(spec_md, domain, slice_name)
    contract_path = output_path / "slice.contract.json"
    contract_path.write_text(contract_json)
    created_files.append(str(contract_path))

    # Generate skeleton files
    templates_dir = Path(__file__).parent.parent / "templates"

    files_to_generate = [
        ("handler.py.j2", "handler.py"),
        ("service.py.j2", "service.py"),
        ("repository.py.j2", "repository.py"),
        ("schemas.py.j2", "schemas.py"),
        ("test_slice.py.j2", "tests/test_slice.py"),
    ]

    for template_name, output_name in files_to_generate:
        template_path = templates_dir / template_name

        if template_path.exists():
            with open(template_path, "r") as f:
                template_str = f.read()

            # Create template with custom filter
            from jinja2 import Environment
            env = Environment()
            env.filters['to_camel_case'] = to_camel_case
            template = env.from_string(template_str)

            content = template.render(
                domain=domain,
                slice_name=slice_name,
                func_spec=func_spec
            )

            file_path = output_path / output_name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
            created_files.append(str(file_path))

    # Create __init__.py files
    init_files = [
        output_path / "__init__.py",
        output_path / "tests" / "__init__.py"
    ]

    for init_file in init_files:
        init_file.parent.mkdir(parents=True, exist_ok=True)
        if not init_file.exists():
            init_file.write_text('"""Generated slice"""')
            created_files.append(str(init_file))

    return created_files

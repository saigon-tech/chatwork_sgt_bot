import click
from src.main import create_app
from src.extensions import db
from src.model.config import Config

app = create_app()
db.app = app


@click.group()
def cli():
    """Database related commands."""
    pass


@cli.command()
@click.argument("action_name")
@click.argument("key_value_pairs", nargs=-1)
def set(action_name, key_value_pairs):
    """Set (add or update) config key-value pairs for a specific action."""
    with app.app_context():
        for pair in key_value_pairs:
            try:
                key, value = pair.split("=", 1)
            except ValueError:
                click.echo(f"Error: Invalid format for '{pair}'. Use 'key=value'.")
                continue

            full_key = f"{action_name.upper()}.{key}"
            config = Config.query.filter_by(key=full_key).first()
            if config:
                config.value = value
                click.echo(f"Updated: {full_key} = {value}")
            else:
                config = Config(key=full_key, value=value)
                db.session.add(config)
                click.echo(f"Added: {full_key} = {value}")
        db.session.commit()


@cli.command()
@click.option("--action", help="Filter configs by action name")
def show(action):
    """Show all config key-value pairs, optionally filtered by action."""
    with app.app_context():
        query = Config.query
        if action:
            query = query.filter(Config.key.startswith(f"{action.upper()}."))

        configs = query.all()
        if configs:
            click.echo("Config entries:")
            for config in configs:
                click.echo(f"  {config.key} = {config.value}")
        else:
            click.echo("No config entries found.")


@cli.command()
@click.argument("action_name")
@click.argument("keys", nargs=-1)
def delete(action_name, keys):
    """Delete config entries by keys for a specific action."""
    with app.app_context():
        for key in keys:
            full_key = f"{action_name.upper()}.{key}"
            config = Config.query.filter_by(key=full_key).first()
            if config:
                db.session.delete(config)
                click.echo(f"Deleted: {full_key}")
            else:
                click.echo(f"Not found: {full_key}")
        db.session.commit()


cli.add_command(set)
cli.add_command(show)
cli.add_command(delete)

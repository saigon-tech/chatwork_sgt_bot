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
@click.argument("key_value_pairs", nargs=-1)
def set(key_value_pairs):
    """Set (add or update) config key-value pairs."""
    with app.app_context():
        for pair in key_value_pairs:
            try:
                key, value = pair.split("=", 1)
            except ValueError:
                click.echo(f"Error: Invalid format for '{pair}'. Use 'key=value'.")
                continue

            config = Config.query.filter_by(key=key).first()
            if config:
                config.value = value
                click.echo(f"Updated: {key} = {value}")
            else:
                config = Config(key=key, value=value)
                db.session.add(config)
                click.echo(f"Added: {key} = {value}")
        db.session.commit()


@cli.command()
def show():
    """Show all config key-value pairs."""
    with app.app_context():
        configs = Config.query.all()
        if configs:
            click.echo("Config entries:")
            for config in configs:
                click.echo(f"  {config.key} = {config.value}")
        else:
            click.echo("No config entries found.")


@cli.command()
@click.argument("keys", nargs=-1)
def delete(keys):
    """Delete config entries by keys."""
    with app.app_context():
        for key in keys:
            config = Config.query.filter_by(key=key).first()
            if config:
                db.session.delete(config)
                click.echo(f"Deleted: {key}")
            else:
                click.echo(f"Not found: {key}")
        db.session.commit()


cli.add_command(set)
cli.add_command(show)
cli.add_command(delete)

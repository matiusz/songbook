import click

@click.group()
def cli():
    pass

@click.command()
@click.option('--port', default=8808, help='port to launch the app on')
def run_flask(port):
    """
    Start Flask application
    """
    from . import run_flask as app
    app.main(port)

@click.command()
def freeze_flask():
    """
    Create static version of Flask app
    """
    from . import freeze_flask as app
    app.main()

@click.command()
def create_pdf():
    """
    Create PDF from data
    """
    from . import create_pdf as app
    app.main()

@click.command()
def create_tex():
    """
    Create LaTeX file from data
    """
    from . import create_tex as app
    app.main()

@click.command()
def run_gui():
    """
    Start GUI application
    """
    from . import run_gui as app
    app.main()

cli.add_command(run_flask)
cli.add_command(freeze_flask)
cli.add_command(create_pdf)
cli.add_command(create_tex)
cli.add_command(run_gui)


if __name__=="__main__":
    cli()
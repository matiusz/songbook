import click

@click.group()
def cli():
    pass

@click.command()
@click.option('--port', default=8808, help='port to launch the app on')
def run_flask(port):
    from . import run_flask as app
    app.main(port)

@click.command()
def freeze_flask():
    from . import freeze_flask as app
    app.main()

@click.command()
def create_pdf():
    from . import create_pdf as app
    app.main()

@click.command()
def create_tex():
    from . import create_tex as app
    app.main()

cli.add_command(run_flask)
cli.add_command(freeze_flask)
cli.add_command(create_pdf)
cli.add_command(create_tex)


if __name__=="__main__":
    cli()
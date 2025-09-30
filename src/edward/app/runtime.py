from edward.infra.config import Settings

class App:
    def __init__(self, settings: Settings):
        self.settings = settings

    def run(self):
        # TODO: wire UI/CLI -> features here (e.g., edward.adapters.presentation.ui)
        pass

def bootstrap() -> App:
    settings = Settings.from_env()
    return App(settings)
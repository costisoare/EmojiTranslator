from abc import ABC, abstractmethod

class BaseLDA(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def load_model(self, dir_name, file_name):
        pass

    @abstractmethod
    def save_model(self, model, dir_name, file_name):
        pass

    @abstractmethod
    def predict_topic(self, text, best_k=2):
        pass

    @abstractmethod
    def create_model(self):
        pass
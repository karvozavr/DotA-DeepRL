import os
from collections import deque
import pickle


class ReplayBuffer:
    """
    Replay buffer for storing sampled data.
    """
    __slots__ = ('data', 'filename')

    def __init__(self, directory='./', max_size=1000000):
        """
        Create new buffer with given params.
        :param directory: directory to work in
        :param max_size: maximal size of a buffer
        """
        self.filename = os.path.join(directory, 'replay_buffer.pkl')
        self.data = deque(maxlen=max_size)

    def save_data(self):
        """
        Save buffer data to file.
        """
        with open(self.filename, 'wb') as output_file:
            pickle.dump(obj=self.data, file=output_file)

    def load_data(self):
        """
        Load buffer data from file.
        """
        with open(self.filename, 'rb') as input_file:
            self.data = pickle.load(file=input_file)

    def __len__(self):
        """
        :return: length of this buffer
        """
        return len(self.data)

    def append(self, element):
        """
        Add single element to buffer.
        :param element: element to add
        """
        self.data.append(element)

    def extend(self, elements):
        """
        Extend buffer with list of elements
        :param elements: list of elements
        """
        self.data.extend(elements)

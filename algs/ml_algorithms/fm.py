import numpy as np

from algs.utils import compute_mse
from algs.utils import sigmoid


def compute_mse(y1, y2):
    if len(y1) != len(y2):
        raise ValueError("y1.length != y2.length")
    y1 = list(y1)
    y2 = list(y2)
    return sum([(y1[i] - y2[i]) ** 2 for i in range(len(y1))]) / len(y1)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


class FM:
    def __init__(self, k=3, task_object='regression', max_iter=100, learning_rate=0.01, bias=0.01, verbose=True):
        self.k = k
        self.task_object = task_object
        self.max_iter = max_iter
        self.learning_rate = learning_rate
        self.v = None
        self.w = None
        self.b = bias
        self.verbose = verbose

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        M, N = x.shape
        self.v = np.random.normal(0, 0.1, [self.k, N])
        self.w = np.random.normal(0, 0.1, N)
        for _iter in range(self.max_iter):
            dv = np.zeros([self.k, N])
            dw = np.zeros(N)
            db = 0
            y_hat = self.predict(x)
            if self.verbose:
                print("################################")
                print("iter{},  训练误差:".format(_iter), compute_mse(y, y_hat))
            for m in range(M):
                diff = y[m] - y_hat[m]
                dw += -0.5 * diff * x[m]
                db += -0.5 * diff

                dv += -0.5 * diff * (
                        np.matmul(np.matmul(self.v, x[m]).reshape(-1, 1), x[m].reshape(1, -1)) - x[m] ** 2 * self.v)

            self.w -= self.learning_rate * dw / m
            self.b -= self.learning_rate * db / m
            self.v -= self.learning_rate * dv / m

    def _product(self, x: np.ndarray):
        """
        :param x: shape [1,n]
        """
        res = 0
        for k in range(self.v.shape[0]):
            tmp = np.array([self.v[k][i] * x[i] for i in range(len(x))])
            res += np.sum(tmp) ** 2 - np.sum(tmp ** 2)
        return 0.5 * res

    def _predict(self, x: np.ndarray):
        """
        :param x: shape [1,n]
        """
        return self.b + np.dot(x, self.w) + self._product(x)

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        """
        :param x: shape [m,n]
        """
        if self.task_object == "regression":
            raise KeyError("no probability in regression task")
        return np.array([sigmoid(self._predict(x[i])) for i in range(len(x))])

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        :param x: shape [m,n]
        """
        if self.task_object == "regression":
            res = [self._predict(x[i]) for i in range(len(x))]
        elif self.task_object == "classification":
            temp = self.predict_proba(x)
            res = (temp > 0.5) * 1
        else:
            raise KeyError("task_object should be regression or classification")
        return np.array(res)

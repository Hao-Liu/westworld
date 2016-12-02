import tensorflow as tf

class Brain(object):
    def __init__(self, world):
        self.world = world
        self.session = tf.Session()
        inputs = tf.placeholder(tf.float32, [256])

import tensorflow as tf
import tflearn

class Brain(object):
    def __init__(self, world, num_actions=2, learning_rate=0.001):
        self.world = world
        self.session = tf.Session()

        self.s = tf.placeholder(tf.float32, [None, 256])
        net = tflearn.fully_connected(self.s, 256, activation='relu')
        self.q_values = tflearn.fully_connected(net, num_actions)
        self.network_params = tf.trainable_variables()

        self.a = tf.placeholder("float", [None, num_actions])
        self.y = tf.placeholder("float", [None])
        action_q_values = tf.reduce_sum(tf.mul(self.q_values, self.a), reduction_indices=1)
        cost = tflearn.mean_square(action_q_values, self.y)
        optimizer = tf.train.RMSPropOptimizer(learning_rate)
        grad_update = optimizer.minimize(cost, var_list=self.network_params)

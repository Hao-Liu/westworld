import tensorflow as tf
import tflearn

class Brain(object):
    def __init__(self, world, num_actions=2, learning_rate=0.001):
        self.world = world
        self.session = tf.Session()

        self.s = tf.placeholder(tf.float32, [None, 10])

        net = tflearn.fully_connected(self.s, 256, activation='relu')
        self.q_values = tflearn.fully_connected(net, num_actions)
        network_params = tf.trainable_variables()

        self.st = tf.placeholder(tf.float32, [None, 10])
        target_net = tflearn.fully_connected(self.st, 256, activation='relu')
        self.target_q_values = tflearn.fully_connected(target_net, num_actions)
        target_network_params = tf.trainable_variables()[len(network_params):]

        self.reset_target_network_params = \
            [target_network_params[i].assign(network_params[i])
             for i in range(len(target_network_params))]

        self.a = tf.placeholder("float", [None, num_actions])
        self.y = tf.placeholder("float", [None])
        action_q_values = tf.reduce_sum(
                tf.mul(self.q_values, self.a),
                reduction_indices=1)
        cost = tflearn.mean_square(action_q_values, self.y)
        optimizer = tf.train.RMSPropOptimizer(learning_rate)
        self.grad_update = optimizer.minimize(cost, var_list=network_params)

        self.session.run(tf.initialize_all_variables())

    def get_action(self, vision):
        print(vision)
        readout = self.q_values.eval(
                session=self.session,
                feed_dict={self.s: [vision]}
                )
        print(readout)

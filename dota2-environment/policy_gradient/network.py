import tensorflow as tf


class Network:
    __slots__ = ('replay_buffer', 'model', 'predict', 'train')

    @staticmethod
    def pg_loss(normalized_rewards):
        def pg_loss(y_true, y_pred):
            probabilities = tf.losses.softmax_cross_entropy(logits=y_pred, onehot_labels=y_true)
            return tf.reduce_mean(tf.mul(probabilities, normalized_rewards))

        return pg_loss

    def build(self, input_shape=172, output_shape=25, learning_rate=0.01):
        onehot_actions = tf.placeholder(dtype='float32', shape=(None, output_shape), name='rewards')
        input_layer = tf.placeholder(dtype='float32', shape=(None, input_shape), name='input')
        normalized_rewards = tf.placeholder(dtype='float32', shape=(None,), name='rewards')

        # network
        layer1 = tf.layers.dense(inputs=input_layer, units=input_shape, activation=tf.nn.selu)
        layer2 = tf.layers.dense(inputs=layer1, units=input_shape, activation=tf.nn.selu)
        layer3 = tf.layers.dense(inputs=layer2, units=input_shape, activation=tf.nn.selu)
        layer4 = tf.layers.dense(inputs=layer3, units=input_shape, activation=tf.nn.selu)

        # output TODO activation
        logits = tf.layers.dense(inputs=layer4, units=output_shape, activation=None)

        # loss
        probabilities = tf.losses.softmax_cross_entropy(onehot_labels=onehot_actions, logits=logits)
        loss = tf.reduce_mean(tf.mul(probabilities, normalized_rewards))

        # predict operation
        self.predict = tf.nn.softmax(logits=logits)

        # train operation
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
        train_op = optimizer.minimize(loss=loss, global_step=tf.train.global_step())
        self.train = train_op

    def __init__(self, replay_buffer, input_shape=172, output_shape=25, learning_rate=0.01):
        self.replay_buffer = replay_buffer
        self.predict = None
        self.train = None
        self.build()

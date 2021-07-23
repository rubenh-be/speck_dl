import tensorflow as tf
from tensorflow import keras
import speck

x_train, y_train = speck.make_train_data(10**7, 5) 
x_val, y_val = speck.make_train_data(10**6, 5)
class SpeckModel(keras.Model):
    def __init__(self, depth=10, **kwargs):
        super(SpeckModel, self).__init__(**kwargs)

        self.block1 = Block1()
        self.res_tower = [Block2i() for _ in range(depth)]
        self.block3 = Block3()

    def call(self, inputs, training=False):
        x = self.block1(inputs)
        for res_block in self.res_tower:
            x = res_block(x)
        x = self.block3(x, is_training=training)

        return x


class Block1(tf.Module):
    def __init__(self, **kwargs):
        super(Block1, self).__init__(**kwargs)

        # Creating layers
        self.conv = keras.layers.Conv1D(filters=32, kernel_size=1)
        self.bn = keras.layers.BatchNormalization()
        
        def __call__(self, x, is_training):

            # Building the block
            x = self.conv(x)
            x = self.bn(x, training=is_training)
            x= tf.nn.relu(x)

            return x

class Block2i(tf.Module):
    def __init__(self, filter_num=32, **kwargs):
        super(Block2i, self).__init__(**kwargs)

        # Creating layers
        self.conv1 = keras.layers.Conv1D(filters=filter_num,
                                         kernel_size=3,
                                         padding="same")
        self.bn1 = keras.layers.BatchNormalization()

        self.conv2 = keras.layers.Conv1D(filters=filter_num,
                                         kernel_size=3,
                                         padding="same")
        self.bn2 = keras.layers.BatchNormalization()

        def __call__(self, x, is_training):
            # Saving x to create shortcut
            shortcut = x
        
            # Building the Residual block
            x = self.conv1(x)
            x = self.bn1(x, training=is_training)
            x = tf.nn.relu(x)

            x = self.conv2(x)
            x = self.bn2(x, training=is_training)
            x = tf.nn.relu(x)

            # returning x with the shortcut added
            return x + shortcut


class Block3(tf.Module):
    def __init__(self, **kwargs):
        super(Block3, self).__init__(**kwargs)

        # Creating layers

        self.flatten = keras.layers.Flatten()

        self.dense1 = keras.layers.Dense(64)
        self.bn1 = keras.layers.BatchNormalization()

        self.dense2 = keras.layers.Dense(64)
        self.bn2 = keras.layers.BatchNormalization()

        self.final = keras.layers.Dense(1)

    def __call__(self, x, is_training):

        # Building the block
        x = self.flatten(x)

        x = self.dense1(x)
        x = self.bn1(x, training=is_training)
        x = tf.nn.relu(x)

        x = self.dense2(x)
        x = self.bn2(x, training=is_training)
        x = tf.nn.relu(x)

        x = self.final(x)
        x = tf.nn.sigmoid(x)

        return x


        
        


model = SpeckModel()

print("Creating jpg...")
tf.keras.utils.plot_model(
    model, to_file='model.png', show_shapes=False, show_dtype=False,
    show_layer_names=True, rankdir='TB', expand_nested=True, dpi=150
)
print("yeet")




    


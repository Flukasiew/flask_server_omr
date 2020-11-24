import tensorflow as tf
import numpy as np
import os


class ModelHandler:
    def __init__(self):
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        tf.reset_default_graph()
        # config = tf.ConfigProto(device_count={"CPU": 0})
        # sess = tf.Session(config=config)
        # self.sess = tf.InteractiveSession(config=config)
        self.sess = tf.InteractiveSession()
        dict_file = open("./app/model/vocab.txt", "r")
        dict_list = dict_file.read().splitlines()
        self.int2word = dict()
        for word in dict_list:
            word_idx = len(self.int2word)
            self.int2word[word_idx] = word
        dict_file.close()
        saver = tf.train.import_meta_graph("./app/model/night_model-62000.meta")
        saver.restore(self.sess, "./app/model/night_model-62000")
        self.graph = tf.get_default_graph()
        self.input = self.graph.get_tensor_by_name("model_input:0")
        self.seq_len = self.graph.get_tensor_by_name("seq_lengths:0")
        self.rnn_keep_prob = self.graph.get_tensor_by_name("keep_prob:0")
        self.height_tensor = self.graph.get_tensor_by_name("input_height:0")
        self.width_reduction_tensor = self.graph.get_tensor_by_name("width_reduction:0")
        self.logits = tf.get_collection("logits")[0]

        self.WIDTH_REDUCTION, self.HEIGHT = self.sess.run(
            [self.width_reduction_tensor, self.height_tensor]
        )
        self.decoded, _ = tf.nn.ctc_greedy_decoder(self.logits, self.seq_len)

    def predict(self, image):
        def sparse_tensor_to_strs(sparse_tensor):
            indices = sparse_tensor[0][0]
            values = sparse_tensor[0][1]
            dense_shape = sparse_tensor[0][2]

            strs = [[] for i in range(dense_shape[0])]

            string = []
            ptr = 0
            b = 0

            for idx in range(len(indices)):
                if indices[idx][0] != b:
                    strs[b] = string
                    string = []
                    b = indices[idx][0]

                string.append(values[ptr])

                ptr = ptr + 1

            strs[b] = string

            return strs

        # Function for Filip
        image = np.asarray(image).reshape(1, image.shape[0], image.shape[1], 1)
        seq_lengths = [image.shape[2] / self.WIDTH_REDUCTION]
        prediction = self.sess.run(
            self.decoded,
            feed_dict={
                self.input: image,
                self.seq_len: seq_lengths,
                self.rnn_keep_prob: 1.0,
            },
        )
        int_predictions = sparse_tensor_to_strs(prediction)
        str_prediction = " ".join([self.int2word[w] for w in int_predictions[0]])

        return str_prediction

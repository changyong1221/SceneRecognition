# -*- coding:utf-8 -*-
"""
Created on Wed Jul 26 18:17:37 2017

@author: hjxu
"""
#%%

#去掉不必要的warning　message
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import numpy as np
import tensorflow as tf
#import input_data
import model
import create_records as cr
#%%

N_CLASSES = 5
IMG_W = 208  # resize the image, if the input image is too large, training will be very slow.
IMG_H = 208
BATCH_SIZE = 32
CAPACITY = 1500
# CAPACITY = 160 32 46 
MAX_STEP = 300 # with current parameters, it is suggested to use MAX_STEP>10k
learning_rate = 0.001 # with current parameters, it is suggested to use learning rate<0.0001


#%%
def run_training1():
    
    # you need to change the directories to yours.
#    train_dir = '/home/hjxu/PycharmProjects/01_cats_vs_dogs/data/train/'
    logs_train_dir = '/home/scy/eclipse-workspace/PythonProject/src/12yue3ri/logs/'
#    
#    train, train_label = input_data.get_files(train_dir)
    tfrecords_file = '/home/scy/eclipse-workspace/PythonProject/src/12yue3ri/my_train2.tfrecords'
    train_batch, train_label_batch = cr.read_and_decode(tfrecords_file, batch_size=BATCH_SIZE)
    train_batch = tf.cast(train_batch,dtype=tf.float32)
    train_label_batch = tf.cast(train_label_batch,dtype=tf.int64)
    
    train_logits = model.inference(train_batch, BATCH_SIZE, N_CLASSES)
    train_loss = model.losses(train_logits, train_label_batch)        
    train_op = model.trainning(train_loss, learning_rate)
    train__acc = model.evaluation(train_logits, train_label_batch)
       
    summary_op = tf.summary.merge_all()
    sess = tf.Session()
    train_writer = tf.summary.FileWriter(logs_train_dir, sess.graph)
    saver = tf.train.Saver()
    
    sess.run(tf.global_variables_initializer())
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    
    try:
        for step in np.arange(MAX_STEP):
            if coord.should_stop():
                    break
            _, tra_loss, tra_acc = sess.run([train_op, train_loss, train__acc])
               
            if step % 5 == 0:
                print('Step %d, train loss = %.2f, train accuracy = %.2f%%' %(step, tra_loss, tra_acc*100.0))
                summary_str = sess.run(summary_op)
                train_writer.add_summary(summary_str, step)
        saver.save(sess, 'net/mydataset_net.ckpt')
#             if step % 4 == 0 or (step + 1) == MAX_STEP:
#                 checkpoint_path = os.path.join(logs_train_dir, 'model.ckpt')
#                 saver.save(sess, checkpoint_path, global_step=step)
                
    except tf.errors.OutOfRangeError:
        print('Done training -- epoch limit reached')
    finally:
        coord.request_stop()
        
    coord.join(threads)
    sess.close()
    
run_training1()

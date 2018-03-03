#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/3 18:47
# @File    : q4.py
# @Author  : NusLuoKe

import numpy as np
import scipy.io
from numpy import exp
from numpy import log
from numpy.linalg import inv

# load the given spam data
spam_data_path = 'T:/EE5907R/spamData.mat'
spam_data = scipy.io.loadmat(spam_data_path)

# print to see some basic information
print(spam_data.keys())

print("length of training set is:", len(spam_data['Xtrain']))
print("length of test set is:", len(spam_data['Xtest']))

print("shape of x_train: ", spam_data['Xtrain'].shape)
print("shape of y_train:", spam_data['ytrain'].shape)
print("shape of x_test:", spam_data['Xtest'].shape)
print("shape of y_test:", spam_data['ytest'].shape)

# load data
x_train = spam_data['Xtrain']
x_test = spam_data['Xtest']
y_test = spam_data['ytest']
y_train = spam_data['ytrain']


# binarize features
def binarize_feature(mail_array):
    return 1 * (mail_array > 0)


# z-normalise features
def z_normalization(mail_array):
    colum_mean = np.mean(mail_array, axis=0)
    colum_std = np.std(mail_array, axis=0)
    return (mail_array - colum_mean) / colum_std


# log-normalise features
def log_transform(mail_array):
    log_mail_array = log(mail_array + 0.1)
    return log_mail_array


x_train_binarization = binarize_feature(x_train)
x_test_binarization = binarize_feature(x_test)

x_train_znorm = z_normalization(x_train)
x_test_znorm = z_normalization(x_test)

x_train_logtrans = log_transform(x_train)
x_test_logtrans = log_transform(x_test)

k_1 = np.arange(1, 10, 1)
k_2 = np.arange(10, 105, 5)
k_value = np.hstack((k_1, k_2))


##############################################################
# norm_z
k = 10
mail_pred = []
for mail_a_id in range(len(x_train_znorm)):
    mail_a = x_train_znorm[mail_a_id]
    dist_mail_single_a = []
    dist_mail_all_a = []
    for mail_b_id in range(len(x_train_znorm)):
        mail_b = x_train_znorm[mail_b_id]

        a = ((mail_a - mail_b)**2)
        b = np.sum(a)
        dist_a_to_b = b**0.5

        dist_mail_single_a.append(dist_a_to_b)  # 找到了a邮件距离别的邮件的距离
        
    dist_small_to_big = np.argsort(dist_mail_single_a)  # 找到了距离最近的K封邮件的索引

    spam_counter = 0
    mail_index = dist_small_to_big[:k]
    for i in mail_index:
        if y_train[i] == 1:
            spam_counter += 1

    p_spam = spam_counter / k
    print(p_spam)

    if p_spam <= 0.5:
        y_pred = 0
    elif p_spam > 0.5:
        y_pred = 1
    mail_pred.append(y_pred)

print(len(mail_pred))
print(mail_pred)



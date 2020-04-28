import os
from collections import defaultdict
import shutil
import sys
import random
from models import tf_idf, w2v_w_tf_idf


def rem_acc(acc_train, acc_test, label):
    if acc_train > stat[label]['train']['max']:
        stat[label]['train']['max'] = acc_train
    if acc_train < stat[label]['train']['min']:
        stat[label]['train']['min'] = acc_train
    if acc_test > stat[label]['test']['max']:
        stat[label]['test']['max'] = acc_test
    if acc_test < stat[label]['test']['min']:
        stat[label]['test']['min'] = acc_test
    stat[label]['train']['avg'] += acc_train
    stat[label]['test']['avg'] += acc_test
    return


# Выбор каталога данных
root = os.path.join(os.curdir, 'data')

category_names = [category for category in os.listdir(root)]
combinations = defaultdict(list)
for i in range(2, len(category_names) + 1):
    for j in range(20):
        combinations[i].append(random.sample(category_names, k=i))

total_numb_combinations = 0
for i in range(2, len(category_names) + 1):
    print('Numb. of categories\t|\tNumb. of combinations')
    print('{}:\t\t\t{}'.format(i, len(combinations[i])))
    total_numb_combinations += len(combinations[i])
    print('')

for i in range(2, len(category_names) + 1):
    print('Numb. of categories\t|\tCombinations')
    print('{}:\t\t\t{}'.format(i, combinations[i]))
    print('')

# exit(0)

with open('all_cat_res.txt', 'a') as results:
    results.write('n_categories\t' +
                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['svm_lin_tfidf'] * 6) +
                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['svm_lin_tfidf_w2v'] * 6) +
                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['svm_lin_tfidf_w2v_c'] * 6) +

                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['svm_rbf_tfidf'] * 6) +
                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['svm_rbf_tfidf_w2v'] * 6) +
                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['svm_rbf_tfidf_w2v_c'] * 6) +

                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['knn_tfidf'] * 6) +
                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['knn_tfidf_w2v'] * 6) +
                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['knn_tfidf_w2v_c'] * 6) +

                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['rfc_tfidf'] * 6) +
                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['rfc_tfidf_w2v'] * 6) +
                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['rfc_tfidf_w2v_c'] * 6) +

                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['mlp_relu_tfidf'] * 6) +
                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['mlp_relu_tfidf_w2v'] * 6) +
                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['mlp_relu_tfidf_w2v_c'] * 6) +

                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['mlp_logistic_tfidf'] * 6) +
                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['mlp_logistic_tfidf_w2v'] * 6) +
                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['mlp_logistic_tfidf_w2v_c'] * 6) +

                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['mlp_tanh_tfidf'] * 6) +
                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\t'.format(
                      *['mlp_tanh_tfidf_w2v'] * 6) +
                  '{}_train_max\t{}_train_avg\t{}_train_min\t{}_test_max\t{}_test_avg\t{}_test_min\n'.format(
                      *['mlp_tanh_tfidf_w2v_c'] * 6)
                  )

numb_combinations = 0

for key in sorted(combinations.keys()):

    stat = {'SVM_LIN_TFIDF': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                              'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'SVM_LIN_TFIDF_W2V': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                                  'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'SVM_LIN_TFIDF_W2V_K': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                                    'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'SVM_RBF_TFIDF': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                              'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'SVM_RBF_TFIDF_W2V': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                                  'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'SVM_RBF_TFIDF_W2V_K': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                                    'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'KNN_TFIDF': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                          'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'KNN_TFIDF_W2V': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                              'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'KNN_TFIDF_W2V_K': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                                'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'RFC_TFIDF': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                          'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'RFC_TFIDF_W2V': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                              'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'RFC_TFIDF_W2V_K': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                                'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'MLP_TFIDF': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                          'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'MLP_TFIDF_W2V': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                              'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'MLP_TFIDF_W2V_K': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                                'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'MLP_LOGIST_TFIDF': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                                 'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'MLP_LOGIST_TFIDF_W2V': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                                     'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'MLP_LOGIST_TFIDF_W2V_K': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                                       'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'MLP_TANH_TFIDF': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                               'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'MLP_TANH_TFIDF_W2V': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                                   'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            'MLP_TANH_TFIDF_W2V_K': {'train': {'max': 0, 'min': sys.maxsize, 'avg': 0},
                                     'test': {'max': 0, 'min': sys.maxsize, 'avg': 0}},
            }
    k = 0
    for combination in combinations[key]:
        if os.path.exists('_tmp_'):
            shutil.rmtree('_tmp_')
        os.mkdir('_tmp_')
        for category_name in list(combination):
            sub_folder = os.path.join('_tmp_', category_name)
            shutil.copytree(os.path.join(root, category_name), sub_folder)

        rem_acc(*tf_idf(data_dir_path='_tmp_', classifier='SVM', svm_kernel='linear', verbose=True),
                label='SVM_LIN_TFIDF')
        rem_acc(*w2v_w_tf_idf(data_dir_path='_tmp_', classifier='SVM', concatenate=False, svm_kernel='linear',
                              verbose=True), label='SVM_LIN_TFIDF_W2V')
        rem_acc(
            *w2v_w_tf_idf(data_dir_path='_tmp_', classifier='SVM', concatenate=True, svm_kernel='linear', verbose=True),
            label='SVM_LIN_TFIDF_W2V_K')

        rem_acc(*tf_idf(data_dir_path='_tmp_', classifier='SVM', svm_kernel='rbf', verbose=True), label='SVM_RBF_TFIDF')
        rem_acc(
            *w2v_w_tf_idf(data_dir_path='_tmp_', classifier='SVM', concatenate=False, svm_kernel='rbf', verbose=True),
            label='SVM_RBF_TFIDF_W2V')
        rem_acc(
            *w2v_w_tf_idf(data_dir_path='_tmp_', classifier='SVM', concatenate=True, svm_kernel='rbf', verbose=True),
            label='SVM_RBF_TFIDF_W2V_K')

        rem_acc(*tf_idf(data_dir_path='_tmp_', classifier='KNN', verbose=True), label='KNN_TFIDF')
        rem_acc(*w2v_w_tf_idf(data_dir_path='_tmp_', classifier='KNN', concatenate=False, verbose=True),
                label='KNN_TFIDF_W2V')
        rem_acc(*w2v_w_tf_idf(data_dir_path='_tmp_', classifier='KNN', concatenate=True, verbose=True),
                label='KNN_TFIDF_W2V_K')

        rem_acc(*tf_idf(data_dir_path='_tmp_', classifier='RFC', verbose=True), label='RFC_TFIDF')
        rem_acc(*w2v_w_tf_idf(data_dir_path='_tmp_', classifier='RFC', concatenate=False, verbose=True),
                label='RFC_TFIDF_W2V')
        rem_acc(*w2v_w_tf_idf(data_dir_path='_tmp_', classifier='RFC', concatenate=True, verbose=True),
                label='RFC_TFIDF_W2V_K')

        rem_acc(*tf_idf(data_dir_path='_tmp_', classifier='MLP', mlp_activation='relu', verbose=True),
                label='MLP_TFIDF')
        rem_acc(*w2v_w_tf_idf(data_dir_path='_tmp_', classifier='MLP', concatenate=False, mlp_activation='relu',
                              verbose=True), label='MLP_TFIDF_W2V')
        rem_acc(*w2v_w_tf_idf(data_dir_path='_tmp_', classifier='MLP', concatenate=True, mlp_activation='relu',
                              verbose=True), label='MLP_TFIDF_W2V_K')

        rem_acc(*tf_idf(data_dir_path='_tmp_', classifier='MLP', mlp_activation='logistic', verbose=True),
                label='MLP_LOGIST_TFIDF')
        rem_acc(*w2v_w_tf_idf(data_dir_path='_tmp_', classifier='MLP', concatenate=False, mlp_activation='logistic',
                              verbose=True), label='MLP_LOGIST_TFIDF_W2V')
        rem_acc(*w2v_w_tf_idf(data_dir_path='_tmp_', classifier='MLP', concatenate=True, mlp_activation='logistic',
                              verbose=True), label='MLP_LOGIST_TFIDF_W2V_K')

        rem_acc(*tf_idf(data_dir_path='_tmp_', classifier='MLP', mlp_activation='tanh', verbose=True),
                label='MLP_TANH_TFIDF')
        rem_acc(*w2v_w_tf_idf(data_dir_path='_tmp_', classifier='MLP', concatenate=False, mlp_activation='tanh',
                              verbose=True), label='MLP_TANH_TFIDF_W2V')
        rem_acc(*w2v_w_tf_idf(data_dir_path='_tmp_', classifier='MLP', concatenate=True, mlp_activation='tanh',
                              verbose=True), label='MLP_TANH_TFIDF_W2V_K')

        k += 1

        shutil.rmtree('_tmp_')

        numb_combinations += 1
        print('||||||||||||||||||||||||||||||||||\t{:.3f}%\t||||||||||||||||||||||||||||||||||'.format(
            numb_combinations / total_numb_combinations * 100
        ))

    for label in stat.keys():
        stat[label]['train']['avg'] /= k
        stat[label]['test']['avg'] /= k

    with open('all_cat_res.txt', 'a') as results:
        results.write('{}\t'.format(key) +
                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['SVM_LIN_TFIDF']['train']['max'],
                                                        stat['SVM_LIN_TFIDF']['train']['avg'],
                                                        stat['SVM_LIN_TFIDF']['train']['min'],
                                                        stat['SVM_LIN_TFIDF']['test']['max'],
                                                        stat['SVM_LIN_TFIDF']['test']['avg'],
                                                        stat['SVM_LIN_TFIDF']['test']['min']) +
                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['SVM_LIN_TFIDF_W2V']['train']['max'],
                                                        stat['SVM_LIN_TFIDF_W2V']['train']['avg'],
                                                        stat['SVM_LIN_TFIDF_W2V']['train']['min'],
                                                        stat['SVM_LIN_TFIDF_W2V']['test']['max'],
                                                        stat['SVM_LIN_TFIDF_W2V']['test']['avg'],
                                                        stat['SVM_LIN_TFIDF_W2V']['test']['min']) +
                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['SVM_LIN_TFIDF_W2V_K']['train']['max'],
                                                        stat['SVM_LIN_TFIDF_W2V_K']['train']['avg'],
                                                        stat['SVM_LIN_TFIDF_W2V_K']['train']['min'],
                                                        stat['SVM_LIN_TFIDF_W2V_K']['test']['max'],
                                                        stat['SVM_LIN_TFIDF_W2V_K']['test']['avg'],
                                                        stat['SVM_LIN_TFIDF_W2V_K']['test']['min']) +

                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['SVM_RBF_TFIDF']['train']['max'],
                                                        stat['SVM_RBF_TFIDF']['train']['avg'],
                                                        stat['SVM_RBF_TFIDF']['train']['min'],
                                                        stat['SVM_RBF_TFIDF']['test']['max'],
                                                        stat['SVM_RBF_TFIDF']['test']['avg'],
                                                        stat['SVM_RBF_TFIDF']['test']['min']) +
                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['SVM_RBF_TFIDF_W2V']['train']['max'],
                                                        stat['SVM_RBF_TFIDF_W2V']['train']['avg'],
                                                        stat['SVM_RBF_TFIDF_W2V']['train']['min'],
                                                        stat['SVM_RBF_TFIDF_W2V']['test']['max'],
                                                        stat['SVM_RBF_TFIDF_W2V']['test']['avg'],
                                                        stat['SVM_RBF_TFIDF_W2V']['test']['min']) +
                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['SVM_RBF_TFIDF_W2V_K']['train']['max'],
                                                        stat['SVM_RBF_TFIDF_W2V_K']['train']['avg'],
                                                        stat['SVM_RBF_TFIDF_W2V_K']['train']['min'],
                                                        stat['SVM_RBF_TFIDF_W2V_K']['test']['max'],
                                                        stat['SVM_RBF_TFIDF_W2V_K']['test']['avg'],
                                                        stat['SVM_RBF_TFIDF_W2V_K']['test']['min']) +

                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['KNN_TFIDF']['train']['max'],
                                                        stat['KNN_TFIDF']['train']['avg'],
                                                        stat['KNN_TFIDF']['train']['min'],
                                                        stat['KNN_TFIDF']['test']['max'],
                                                        stat['KNN_TFIDF']['test']['avg'],
                                                        stat['KNN_TFIDF']['test']['min']) +
                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['KNN_TFIDF_W2V']['train']['max'],
                                                        stat['KNN_TFIDF_W2V']['train']['avg'],
                                                        stat['KNN_TFIDF_W2V']['train']['min'],
                                                        stat['KNN_TFIDF_W2V']['test']['max'],
                                                        stat['KNN_TFIDF_W2V']['test']['avg'],
                                                        stat['KNN_TFIDF_W2V']['test']['min']) +
                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['KNN_TFIDF_W2V_K']['train']['max'],
                                                        stat['KNN_TFIDF_W2V_K']['train']['avg'],
                                                        stat['KNN_TFIDF_W2V_K']['train']['min'],
                                                        stat['KNN_TFIDF_W2V_K']['test']['max'],
                                                        stat['KNN_TFIDF_W2V_K']['test']['avg'],
                                                        stat['KNN_TFIDF_W2V_K']['test']['min']) +

                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['RFC_TFIDF']['train']['max'],
                                                        stat['RFC_TFIDF']['train']['avg'],
                                                        stat['RFC_TFIDF']['train']['min'],
                                                        stat['RFC_TFIDF']['test']['max'],
                                                        stat['RFC_TFIDF']['test']['avg'],
                                                        stat['RFC_TFIDF']['test']['min']) +
                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['RFC_TFIDF_W2V']['train']['max'],
                                                        stat['RFC_TFIDF_W2V']['train']['avg'],
                                                        stat['RFC_TFIDF_W2V']['train']['min'],
                                                        stat['RFC_TFIDF_W2V']['test']['max'],
                                                        stat['RFC_TFIDF_W2V']['test']['avg'],
                                                        stat['RFC_TFIDF_W2V']['test']['min']) +
                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['RFC_TFIDF_W2V_K']['train']['max'],
                                                        stat['RFC_TFIDF_W2V_K']['train']['avg'],
                                                        stat['RFC_TFIDF_W2V_K']['train']['min'],
                                                        stat['RFC_TFIDF_W2V_K']['test']['max'],
                                                        stat['RFC_TFIDF_W2V_K']['test']['avg'],
                                                        stat['RFC_TFIDF_W2V_K']['test']['min']) +

                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['MLP_TFIDF']['train']['max'],
                                                        stat['MLP_TFIDF']['train']['avg'],
                                                        stat['MLP_TFIDF']['train']['min'],
                                                        stat['MLP_TFIDF']['test']['max'],
                                                        stat['MLP_TFIDF']['test']['avg'],
                                                        stat['MLP_TFIDF']['test']['min']) +
                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['MLP_TFIDF_W2V']['train']['max'],
                                                        stat['MLP_TFIDF_W2V']['train']['avg'],
                                                        stat['MLP_TFIDF_W2V']['train']['min'],
                                                        stat['MLP_TFIDF_W2V']['test']['max'],
                                                        stat['MLP_TFIDF_W2V']['test']['avg'],
                                                        stat['MLP_TFIDF_W2V']['test']['min']) +
                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['MLP_TFIDF_W2V_K']['train']['max'],
                                                        stat['MLP_TFIDF_W2V_K']['train']['avg'],
                                                        stat['MLP_TFIDF_W2V_K']['train']['min'],
                                                        stat['MLP_TFIDF_W2V_K']['test']['max'],
                                                        stat['MLP_TFIDF_W2V_K']['test']['avg'],
                                                        stat['MLP_TFIDF_W2V_K']['test']['min']) +

                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['MLP_LOGIST_TFIDF']['train']['max'],
                                                        stat['MLP_LOGIST_TFIDF']['train']['avg'],
                                                        stat['MLP_LOGIST_TFIDF']['train']['min'],
                                                        stat['MLP_LOGIST_TFIDF']['test']['max'],
                                                        stat['MLP_LOGIST_TFIDF']['test']['avg'],
                                                        stat['MLP_LOGIST_TFIDF']['test']['min']) +
                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['MLP_LOGIST_TFIDF_W2V']['train']['max'],
                                                        stat['MLP_LOGIST_TFIDF_W2V']['train']['avg'],
                                                        stat['MLP_LOGIST_TFIDF_W2V']['train']['min'],
                                                        stat['MLP_LOGIST_TFIDF_W2V']['test']['max'],
                                                        stat['MLP_LOGIST_TFIDF_W2V']['test']['avg'],
                                                        stat['MLP_LOGIST_TFIDF_W2V']['test']['min']) +
                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['MLP_LOGIST_TFIDF_W2V_K']['train']['max'],
                                                        stat['MLP_LOGIST_TFIDF_W2V_K']['train']['avg'],
                                                        stat['MLP_LOGIST_TFIDF_W2V_K']['train']['min'],
                                                        stat['MLP_LOGIST_TFIDF_W2V_K']['test']['max'],
                                                        stat['MLP_LOGIST_TFIDF_W2V_K']['test']['avg'],
                                                        stat['MLP_LOGIST_TFIDF_W2V_K']['test']['min']) +

                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['MLP_TANH_TFIDF']['train']['max'],
                                                        stat['MLP_TANH_TFIDF']['train']['avg'],
                                                        stat['MLP_TANH_TFIDF']['train']['min'],
                                                        stat['MLP_TANH_TFIDF']['test']['max'],
                                                        stat['MLP_TANH_TFIDF']['test']['avg'],
                                                        stat['MLP_TANH_TFIDF']['test']['min']) +
                      '{}\t{}\t{}\t{}\t{}\t{}\t'.format(stat['MLP_TANH_TFIDF_W2V']['train']['max'],
                                                        stat['MLP_TANH_TFIDF_W2V']['train']['avg'],
                                                        stat['MLP_TANH_TFIDF_W2V']['train']['min'],
                                                        stat['MLP_TANH_TFIDF_W2V']['test']['max'],
                                                        stat['MLP_TANH_TFIDF_W2V']['test']['avg'],
                                                        stat['MLP_TANH_TFIDF_W2V']['test']['min']) +
                      '{}\t{}\t{}\t{}\t{}\t{}\n'.format(stat['MLP_TANH_TFIDF_W2V_K']['train']['max'],
                                                        stat['MLP_TANH_TFIDF_W2V_K']['train']['avg'],
                                                        stat['MLP_TANH_TFIDF_W2V_K']['train']['min'],
                                                        stat['MLP_TANH_TFIDF_W2V_K']['test']['max'],
                                                        stat['MLP_TANH_TFIDF_W2V_K']['test']['avg'],
                                                        stat['MLP_TANH_TFIDF_W2V_K']['test']['min'])
                      )

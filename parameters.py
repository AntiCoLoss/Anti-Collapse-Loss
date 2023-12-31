import argparse
import os


def basic_training_parameters(parser):
    ### General Training Parameters
    parser.add_argument('--dataset', default='cub200', type=str,
                        help='Dataset to use.')
    parser.add_argument('--use_tv_split', action='store_true',
                        help='Flag. If set, splits training set into a train/validation setup following --tv_split_perc.')
    parser.add_argument('--tv_split_by_samples', action='store_true',
                        help='Whether to split train/validation sets by splitting per class or between classes.')
    parser.add_argument('--tv_split_perc', default=0,  type=float,
                        help='Percentage with which the training dataset is split into training/validation.')
    parser.add_argument('--completed', action='store_true',
                        help='Flag. If set, denotes that the training process has been completed.')
    parser.add_argument('--no_train_metrics', action='store_true',
                        help='Flag. If set, no training metrics are computed and logged.')
    parser.add_argument('--no_test_metrics', action='store_true',
                        help='Flag. If set, no test metrics are computed and logged.')
    #
    parser.add_argument('--evaluation_metrics', nargs='+', default=['e_recall@1', 'e_recall@2', 'e_recall@4', 'e_recall@8',
                                                                    'nmi', 'f1', 'mAP_1000',], type=str,
                        help='Metrics to evaluate performance by.')
    parser.add_argument('--evaltypes', nargs='+', default=['embeds'], type=str,
                        help='The network may produce multiple embeddings (ModuleDict). If the key is listed here, the entry will be evaluated on the evaluation metrics. Note: One may use Combined_embed1_embed2_..._embedn-w1-w1-...-wn to compute evaluation metrics on weighted (normalized) combinations.')
    parser.add_argument('--storage_metrics', nargs='+', default=['e_recall@1'], type=str,
                        help='Improvement in these metrics will trigger checkpointing.')
    parser.add_argument('--store_improvements', action='store_true',
                        help='If set, will store checkpoints whenever the storage metric improves.')
    #
    parser.add_argument('--gpu', default=[0], nargs='+', type=int,
                        help='Random seed for reproducibility.')
    parser.add_argument('--savename', default='group_plus_seed',   type=str,
                        help='Appendix to save folder name if any special information is to be included.')
    parser.add_argument('--source_path', default=os.getcwd()+'/../../Datasets',   type=str,
                        help='Path to training data.')
    parser.add_argument('--save_path', default=os.getcwd()+'/Training_Results', type=str,
                        help='Where to save everything.')
    ### General Optimization Parameters
    parser.add_argument('--lr',  default=0.00001, type=float,
                        help='Learning Rate for network parameters.')
    parser.add_argument('--fc_lr', default=-1, type=float,
                        help='Learning Rate for mlp head parameters. If -1, uses the same base lr.')
    parser.add_argument('--n_epochs', default=150, type=int,
                        help='Number of training epochs.')
    parser.add_argument('--kernels', default=6, type=int,
                        help='Number of workers for pytorch dataloader.')
    parser.add_argument('--bs', default=112 , type=int,
                        help='Mini-Batchsize to use.')
    parser.add_argument('--seed', default=0, type=int,
                        help='Random seed for reproducibility.')
    parser.add_argument('--scheduler', default='step', type=str,
                        help='Type of learning rate scheduling. Currently: step & exp.')
    parser.add_argument('--gamma', default=0.3, type=float,
                        help='Learning rate reduction after --tau epochs.')
    parser.add_argument('--decay', default=0.0004, type=float,
                        help='Weight decay for optimizer.')
    parser.add_argument('--tau', default=[10000],  nargs='+',type=int,
                        help='Stepsize before reducing learning rate.')
    parser.add_argument('--augmentation', default='base', type=str,
                        help='Type of learning rate scheduling. Currently: step & exp.')
    parser.add_argument('--warmup', default=0, type=int,
                        help='Appendix to save folder name if any special information is to be included.')
    #
    parser.add_argument('--evaluate_on_cpu', action='store_true',
                        help='Flag. If set, computed evaluation metrics on CPU instead of GPU.')
    parser.add_argument('--internal_split', default=1, type=float,
                        help='Split parameter used for meta-learning extensions.')
    #
    parser.add_argument('--optim', default='adam', type=str,
                        help='Optimizer to use.')
    parser.add_argument('--loss', default='margin', type=str,
                        help='Trainin objective to use. See folder <criteria> for available methods.')
    parser.add_argument('--batch_mining', default='distance', type=str,
                        help='Batchmining method to use. See folder <batchminer> for available methods.')
    #
    parser.add_argument('--embed_dim', default=128, type=int,
                        help='Embedding dimensionality of the network. Note: dim=128 or 64 is used in most papers.')
    parser.add_argument('--arch', default='resnet50_frozen_normalize',  type=str,
                        help='Underlying network architecture. Frozen denotes that exisiting pretrained batchnorm layers are frozen, and normalize denotes normalization of the output embedding.')
    parser.add_argument('--not_pretrained', action='store_true',
                        help='Flag. If set, does not initialize the backbone network with ImageNet pretraining.')
    parser.add_argument('--use_float16', action='store_true',
                        help='Flag. If set, uses float16-inputs.')
    return parser


def wandb_parameters(parser):
    """
    Parameters for Weights & Biases logging.
    """
    parser.add_argument('--log_online', action='store_true',
                        help='Flag. If set, logs key data to W&B servers.')
    parser.add_argument('--wandb_key', default='<your_wandb_key>', type=str,
                        help='W&B account key.')
    parser.add_argument('--project', default='DiVA_Sample_Runs', type=str,
                        help='W&B Project name.')
    parser.add_argument('--group', default='Sample_Run', type=str,
                        help='W&B Group name - allows you to group multiple seeds within the same group.')
    return parser


def nir_parameters(parser):
    """
    Parameters for Non-isotropy Regularization for Proxy-based DML.
    """
    ### Base NIR parameters
    parser.add_argument('--loss_nir_w_align', default=0.01, type=float,
                        help='Alignment weight between proxy-loss and NF loss.')
    parser.add_argument('--loss_nir_proxy_lrmulti', default=4000, type=float,
                        help='Learning rate multiplier for proxy-based normflow approach.')
    parser.add_argument('--loss_nir_lrmulti', default=50, type=float,
                        help='Learning rate multiplier for normalizing flows header.')
    parser.add_argument('--loss_nir_logmatch', default=1., type=float,
                        help='Weight scale for log_jac_det.')
    parser.add_argument('--loss_nir_pos_alpha', default=1., type=float,
                        help='Positive relation weighting.')
    parser.add_argument('--loss_nir_neg_alpha', default=1., type=float,
                        help='Negative relation weighting.')
    parser.add_argument('--loss_nir_margin', default=0.1, type=float,
                        help='Masking threshold.')
    parser.add_argument('--loss_nir_delta', default=0.2, type=float,
                        help='Scaling threshold in MSIM-style formulation.')
    parser.add_argument('--loss_nir_pair_perc', default=1., type=float,
                        help='Percentage of sample-proxy-pairs to use during training.')
    parser.add_argument('--loss_nir_noise', default=0, type=float,
                        help='Input Noise to NF model.')
    ### Normalizing Flow parameters.
    parser.add_argument('--loss_nir_nf_cond_mode', default='dense', type=str,
                        help='Conditioning mode for normflow model.')
    parser.add_argument('--loss_nir_nf_fc_depth', default=8, type=int,
                        help='Depth of nonlinear FC mapper in NF blocks.')
    parser.add_argument('--loss_nir_nf_fc_width', default=128, type=int,
                        help='Num nodes of nonlinear FC mapper layers in NF blocks.')
    parser.add_argument('--loss_nir_nf_cblocks', default=5, type=int,
                        help='Number of NormFlow blocks.')
    parser.add_argument('--loss_nir_nf_fc_dropout', default=0, type=float,
                        help='Dropout for nonlinear FC mapper.')
    parser.add_argument('--loss_nir_nf_clamp_alpha', default=2., type=float,
                        help='Clamping value.')
    parser.add_argument('--loss_nir_nf_fc_init', default='none', type=str,
                        help='Initializaiton method to use for linear subnets.')
    return parser


def loss_specific_parameters(parser):
    """
    Hyperparameters for various base DML criteria.
    """
    ### Contrastive Loss.
    parser.add_argument('--loss_contrastive_pos_margin', default=0, type=float,
                        help='Positive margin for contrastive pairs.')
    parser.add_argument('--loss_contrastive_neg_margin', default=1, type=float,
                        help='Negative margin for contrastive pairs.')
    ### Triplet-based Losses.
    parser.add_argument('--loss_triplet_margin', default=0.2, type=float,
                        help='Margin for Triplet Loss')

    ### ProxyAnchor.
    parser.add_argument('--loss_oproxy_mode', default='nca', type=str,
                        help='Proxy-method: anchor = ProxyAnchor, nca = ProxyNCA.')
    parser.add_argument('--loss_oproxy_lrmulti', default=2000, type=float,
                        help='Learning rate multiplier for proxies.')
    parser.add_argument('--loss_oproxy_pos_alpha', default=64, type=float,
                        help='Inverted temperature/scaling for positive sample-proxy similarities.')
    parser.add_argument('--loss_oproxy_neg_alpha', default=64, type=float,
                        help='Inverted temperature/scaling for negative sample-proxy similarities.')
    parser.add_argument('--loss_oproxy_pos_delta', default=0.1, type=float,
                        help='Threshold for positive sample-proxy similarities')
    parser.add_argument('--loss_oproxy_neg_delta', default=-0.1, type=float,
                        help='Threshold for negative sample-proxy similarities')

    ### Anti-Collapse Loss
    parser.add_argument('--antico_w', default=1, type=float,
                        help='weight for AntiCo')
    parser.add_argument('--antico_gam1', default=1, type=float,
                        help='Gamma 1 for AntiCo')
    parser.add_argument('--antico_gam2', default=1, type=float,
                        help='Gamma 2 for AntiCo')
    parser.add_argument('--antico_eps', default=0.5, type=float,
                        help='eps for AntiCo')
    parser.add_argument('--antico_type', default='batch_proxy', type=str,
                        help='Classes for AntiCo Loss')
    parser.add_argument('--loss_ac_w_align', default=0.01, type=float,
                        help='Alignment weight between proxy-loss and ac loss.')
    return parser


def batchmining_specific_parameters(parser):
    """
    Hyperparameters for various batchmining methods.
    """
    ### Distance-based_Sampling.
    parser.add_argument('--miner_distance_lower_cutoff', default=0.5, type=float,
                        help='Cutoff distance value below which pairs are ignored.')
    parser.add_argument('--miner_distance_upper_cutoff', default=1.4, type=float,
                        help='Cutoff distance value above which pairs are ignored.')
    ### Spectrum-Regularized Miner.
    parser.add_argument('--miner_rho_distance_lower_cutoff', default=0.5, type=float,
                        help='Same behaviour as with standard distance-based mining.')
    parser.add_argument('--miner_rho_distance_upper_cutoff', default=1.4, type=float,
                        help='Same behaviour as with standard distance-based mining.')
    parser.add_argument('--miner_rho_distance_cp', default=0.2, type=float,
                        help='Probability with which label assignments are flipped.')
    ### Semihard Batchmining.
    parser.add_argument('--miner_semihard_margin', default=0.2, type=float,
                        help='Margin value for semihard mining.')
    return parser


def batch_creation_parameters(parser):
    """
    Parameters for batch sampling methods.
    """
    parser.add_argument('--data_sampler', default='class_random', type=str,
                        help='Batch-creation method. Default <class_random> ensures that for each class, at least --samples_per_class samples per class are available in each minibatch.')
    parser.add_argument('--data_ssl_set', action='store_true',
                        help='Obsolete. Only relevant for SSL-based extensions.')
    parser.add_argument('--samples_per_class', default=2, type=int,
                        help='Number of samples in one class drawn before choosing the next class. Set to >1 for losses other than ProxyNCA.')
    return parser

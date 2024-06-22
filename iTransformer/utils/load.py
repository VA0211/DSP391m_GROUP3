import re
from collections import namedtuple
import argparse

def parse_bash_script(script_content):
    # Define the named tuple for arguments
    Args = namedtuple('Args', [
        'is_training', 'root_path', 'data_path', 'model_id', 'model', 'data', 'features',
        'target', 'freq', 'seq_len', 'label_len', 'pred_len', 'e_layers', 'enc_in', 'dec_in', 'c_out',
        'des', 'd_model', 'd_ff', 'itr', 'target_root_path', 'target_data_path',
        'lradj', 'learning_rate', 'patience', 'moving_avg', 'dropout', 'train_epochs', 'batch_size', 
        # 'do_predict'
    ])

    # Use regex to find all key=value pairs in the bash script content
    pattern = r'--(\S+) ([^\s\\]+)'
    matches = re.findall(pattern, script_content)

    # Convert matches to a dictionary
    args_dict = {key: value for key, value in matches}

    # Convert to named tuple Args
    args = Args(
        is_training=int(args_dict.get('is_training', 0)),
        root_path=args_dict.get('root_path', ''),
        data_path=args_dict.get('data_path', ''),
        model_id=args_dict.get('model_id', ''),
        model=args_dict.get('model', ''),
        data=args_dict.get('data', 'custom'),
        features=args_dict.get('features', ''),
        target=args_dict.get('target', ''),
        freq=args_dict.get('freq', ''),
        seq_len=int(args_dict.get('seq_len', 0)),
        label_len=int(args_dict.get('label_len', 0)),
        pred_len=int(args_dict.get('pred_len', 0)),
        e_layers=int(args_dict.get('e_layers', 0)),
        enc_in=int(args_dict.get('enc_in', 0)),
        dec_in=int(args_dict.get('dec_in', 0)),
        c_out=int(args_dict.get('c_out', 0)),
        des=args_dict.get('des', 'Exp'),
        d_model=int(args_dict.get('d_model', 0)),
        d_ff=int(args_dict.get('d_ff', 0)),
        itr=int(args_dict.get('itr', 0)),
        target_root_path=args_dict.get('target_root_path', ''),
        target_data_path=args_dict.get('target_data_path', ''),
        lradj=args_dict.get('lradj', 'type1'),
        learning_rate=float(args_dict.get('learning_rate', 0)),
        patience=int(args_dict.get('patience', 0)),
        moving_avg=int(args_dict.get('moving_avg', 0)),
        dropout=float(args_dict.get('dropout', 0)),
        train_epochs=int(args_dict.get('train_epochs', 0)),
        batch_size=int(args_dict.get('batch_size', 0)),
        # do_predict='--do_predict' in script_content  # Check if '--do_predict' is present in the script content
    )

    # Convert named tuple to argparse.Namespace
    args_namespace = argparse.Namespace(**args._asdict())

    return args_namespace

def get_default_config():
    parser = argparse.ArgumentParser(description='iTransformer')

    # basic config
    parser.add_argument('--is_training', type=int, required=False, default=1, help='status')
    parser.add_argument('--model_id', type=str, required=False, default='Exchange_96_96', help='model id')
    parser.add_argument('--model', type=str, required=False, default='iTransformer',
                        help='model name, options: [iTransformer, iInformer, iReformer, iFlowformer, iFlashformer]')

    # data loader
    parser.add_argument('--data', type=str, required=False, default='custom', help='dataset type')
    parser.add_argument('--root_path', type=str, default='D:/FPT/SU24/DSP391m/code/crawl/data/clean/', help='root path of the data file')
    parser.add_argument('--data_path', type=str, default='df_combine.csv', help='data csv file')
    parser.add_argument('--features', type=str, default='S',
                        help='forecasting task, options:[M, S, MS]; M:multivariate predict multivariate, S:univariate predict univariate, MS:multivariate predict univariate')
    parser.add_argument('--target', type=str, default='Sell', help='target feature in S or MS task')
    parser.add_argument('--freq', type=str, default='h',
                        help='freq for time features encoding, options:[s:secondly, t:minutely, h:hourly, d:daily, b:business days, w:weekly, m:monthly], you can also use more detailed freq like 15min or 3h')
    parser.add_argument('--checkpoints', type=str, default='./checkpoints/', help='location of model checkpoints')

    # forecasting task
    parser.add_argument('--seq_len', type=int, default=96, help='input sequence length')
    parser.add_argument('--label_len', type=int, default=48, help='start token length') # no longer needed in inverted Transformers
    parser.add_argument('--pred_len', type=int, default=96, help='prediction sequence length')

    # model define
    parser.add_argument('--enc_in', type=int, default=7, help='encoder input size')
    parser.add_argument('--dec_in', type=int, default=7, help='decoder input size')
    parser.add_argument('--c_out', type=int, default=7, help='output size') # applicable on arbitrary number of variates in inverted Transformers
    parser.add_argument('--d_model', type=int, default=128, help='dimension of model')
    parser.add_argument('--n_heads', type=int, default=8, help='num of heads')
    parser.add_argument('--e_layers', type=int, default=2, help='num of encoder layers')
    parser.add_argument('--d_layers', type=int, default=1, help='num of decoder layers')
    parser.add_argument('--d_ff', type=int, default=128, help='dimension of fcn')
    parser.add_argument('--moving_avg', type=int, default=25, help='window size of moving average')
    parser.add_argument('--factor', type=int, default=1, help='attn factor')
    parser.add_argument('--distil', action='store_false',
                        help='whether to use distilling in encoder, using this argument means not using distilling',
                        default=True)
    parser.add_argument('--dropout', type=float, default=0.1, help='dropout')
    parser.add_argument('--embed', type=str, default='timeF',
                        help='time features encoding, options:[timeF, fixed, learned]')
    parser.add_argument('--activation', type=str, default='gelu', help='activation')
    parser.add_argument('--output_attention', action='store_true', help='whether to output attention in ecoder')
    parser.add_argument('--do_predict', action='store_true', help='whether to predict unseen future data')

    # optimization
    parser.add_argument('--num_workers', type=int, default=10, help='data loader num workers')
    parser.add_argument('--itr', type=int, default=1, help='experiments times')
    parser.add_argument('--train_epochs', type=int, default=10, help='train epochs')
    parser.add_argument('--batch_size', type=int, default=32, help='batch size of train input data')
    parser.add_argument('--patience', type=int, default=3, help='early stopping patience')
    parser.add_argument('--learning_rate', type=float, default=0.0001, help='optimizer learning rate')
    parser.add_argument('--des', type=str, default='Exp', help='exp description')
    parser.add_argument('--loss', type=str, default='MSE', help='loss function')
    parser.add_argument('--lradj', type=str, default='type1', help='adjust learning rate')
    parser.add_argument('--use_amp', action='store_true', help='use automatic mixed precision training', default=False)

    # GPU
    parser.add_argument('--use_gpu', type=bool, default=False, help='use gpu')
    parser.add_argument('--gpu', type=int, default=0, help='gpu')
    parser.add_argument('--use_multi_gpu', action='store_true', help='use multiple gpus', default=False)
    parser.add_argument('--devices', type=str, default='0,1,2,3', help='device ids of multile gpus')

    # iTransformer
    parser.add_argument('--exp_name', type=str, required=False, default='partial_train',
                        help='experiemnt name, options:[MTSF, partial_train]')
    parser.add_argument('--channel_independence', type=bool, default=False, help='whether to use channel_independence mechanism')
    parser.add_argument('--inverse', action='store_true', help='inverse output data', default=False)
    parser.add_argument('--class_strategy', type=str, default='projection', help='projection/average/cls_token')
    parser.add_argument('--target_root_path', type=str, default='D:/FPT/SU24/DSP391m/code/crawl/data/clean/', help='root path of the data file')
    parser.add_argument('--target_data_path', type=str, default='df_combine.csv', help='data file')
    parser.add_argument('--efficient_training', type=bool, default=False, help='whether to use efficient_training (exp_name should be partial train)') # See Figure 8 of our paper for the detail
    parser.add_argument('--use_norm', type=int, default=True, help='use norm and denorm')
    parser.add_argument('--partial_start_index', type=int, default=0, help='the start index of variates for partial training, '
                                                                          'you can select [partial_start_index, min(enc_in + partial_start_index, N)]')
    return parser

def merge_args(args1, args2):
    # Convert Namespace to dictionary
    dict1 = vars(args1)
    dict2 = vars(args2)
    
    # Merge dictionaries
    merged_dict = dict1.copy()  # Start with all elements from dict1
    for key, value in dict2.items():
        if key not in merged_dict:  # Only add keys from dict2 that are not in dict1
            merged_dict[key] = value
    
    # Convert merged dictionary back to Namespace
    merged_args = argparse.Namespace(**merged_dict)
    return merged_args
export CUDA_VISIBLE_DEVICES=2

model_name=iTransformer

python -u run.py \
  --is_training 1 \
  --root_path D:/FPT/SU24/DSP391m/code/data/ \
  --data_path df_combine.csv \
  --model_id forex_M \
  --model iTransformer \
  --data custom \
  --features MS \
  --target Sell \
  --freq d \
  --seq_len 10 \
  --label_len 5 \
  --pred_len 10 \
  --e_layers 1 \
  --enc_in 4 \
  --dec_in 4 \
  --c_out 4 \
  --des Exp \
  --d_model 128 \
  --d_ff 128 \
  --itr 1 \
  --target_root_path D:/FPT/SU24/DSP391m/code/data/ \
  --target_data_path df_combine.csv \
  --lradj type1 \
  --learning_rate 0.0001 \
  --patience 5 \
  --moving_avg 5 \
  --dropout 0.25 \
  --train_epochs 20 \
  --batch_size 32 \
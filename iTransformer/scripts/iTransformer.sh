export CUDA_VISIBLE_DEVICES=2

model_name=iTransformer

python -u run.py \
  --is_training 1 \
  --root_path D:/FPT/SU24/DSP391m/code/crawl/data/clean/ \
  --data_path df_combine.csv \
  --model_id Exchange_96_96 \
  --model $model_name \
  --data custom \
  --features MS \
  --target 'Sell' \
  --freq 'd' \
  --seq_len 96 \
  --pred_len 96 \
  --e_layers 2 \
  --enc_in 8 \
  --dec_in 8 \
  --c_out 8 \
  --des 'Exp' \
  --d_model 128 \
  --d_ff 128 \
  --itr 1 \
  --target_root_path D:/FPT/SU24/DSP391m/code/crawl/data/clean/ \
  --target_data_path df_combine.csv \
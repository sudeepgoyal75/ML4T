from machine_learning.development.new_regression import new_dataset as ds
from machine_learning.development.linear_regression import calculate_rmse
import machine_learning.development.knn_wrapper as knn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

#building the dataset
print("> building the dataset...")
stock_symbol = '^GSPC'
start_date = '1950-01-01'
end_date = '2017-12-31'
window = 5
dataframe, scaler = ds.bulid_TIs_dataset(stock_symbol, start_date, end_date, window)

#reshaping the dataset
print("\n> reshaping the dataset...")
dataset = dataframe.values
future_gap = 5 #1 trading week
split = 0.8 #80% of the dataset
X_train, Y_train, X_test, Y_test = ds.dataset_reshape(dataset, future_gap, split)

#kNN model
model = knn.knn(5)

#fitting the training data
model.train(X_train, Y_train)

#predictions
predictions = model.query(X_test, normalize=False, addDiff=False)

#evaluating the model on the normalized dataset
rmse = calculate_rmse(predictions, Y_test)
print('Normalized Test RMSE: %.3f' %(rmse))
mape = ds.compute_mape(Y_test, predictions)
print('Normalized Outsample MAPE: %.3f' %(mape))
correlation = np.corrcoef(predictions, Y_test)
print("Normalized Correlation: %.3f"%(correlation[0, 1]))
r2 = r2_score(predictions, Y_test)
print("Normalized Outsample r^2: %.3f"%(r2))

#evaluating the model on the inverse-normalized dataset
predictions = predictions.reshape((predictions.shape[0], 1))
Y_test = Y_test.reshape((Y_test.shape[0], 1))

predictions_inv_scaled = scaler.inverse_transform(predictions)
Y_test_inv_scaled = scaler.inverse_transform(Y_test)

rmse = calculate_rmse(predictions_inv_scaled, Y_test_inv_scaled)
print('\nInverse-Normalized Outsample RMSE: %.3f' %(rmse))
mape = ds.compute_mape(Y_test_inv_scaled, predictions_inv_scaled)
print('Inverse-Normalized Outsample MAPE: %.3f' %(mape))
correlation = np.corrcoef(predictions_inv_scaled.T, Y_test_inv_scaled.T)
print("Inverse-Normalized Outsample Correlation: %.3f"%(correlation[0, 1]))
r2 = r2_score(predictions_inv_scaled, Y_test_inv_scaled)
print("Inverse-Normalized Outsample r^2: %.3f"%(r2))

#plotting
_, ax = plt.subplots()
ax.plot(range(len(predictions_inv_scaled)), predictions_inv_scaled, label='Prediction')
ax.plot(range(len(Y_test_inv_scaled)), Y_test_inv_scaled, label='Actual')
ax.set_xlabel('Trading Day')
ax.set_ylabel('Price')
ax.legend(loc='best')
ax.grid(True)

plt.show()
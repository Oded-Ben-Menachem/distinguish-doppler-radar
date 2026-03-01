from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
import joblib

np.set_printoptions(suppress=True, precision=4)
if __name__ == "__main__":


    x_tennis_ball = np.load('tennis1_for_forest.npy')
    x_soccer_ball = np.load('soccer1_for_forest.npy')
    
    print(x_soccer_ball.shape,x_tennis_ball.shape)#,x_noise.shape)
    X = np.vstack((x_tennis_ball,x_soccer_ball))#,x_noise))

    print(X.shape)

 
    y = np.array(['T'] * x_tennis_ball.shape[0] + ['S'] * x_soccer_ball.shape[0])

    # split for traning and for check
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1)
    # biult the model
    rf_model = RandomForestClassifier(n_estimators=100 ,random_state=42)

    #trainning the model
    rf_model.fit(X_train, y_train)


    #
    predictions = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    feature_names = ['calculate_spectral_bandwidth','calculate_spectral_kurosis','peak_to_average','calculate_spectral_skewness','calculate_spectral_rolloff','total_power']
    importances = rf_model.feature_importances_

    print('Feature Importance:')
    for i in range(len(feature_names)):
        print(f'{feature_names[i]}:{importances[i]}')

    print('-'*30)
    print(f'prediction:{predictions}')
    print(f'accuracy: {accuracy*100:.4f}%')
    joblib.dump(rf_model,'radar_recognize_ball_model.pkl')




   


import feature

feature.build_feature_dataset(300, training_split=0.20)
feature.build_label_file("1")
feature.build_corr_dataset()
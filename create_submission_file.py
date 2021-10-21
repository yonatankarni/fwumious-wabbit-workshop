import gzip

def create_submission_file(test_preds, submission_file, test_data='test.fw.gz'):
    display_id_col_idx = 18
    ad_id_col_idx = 9
    
    last_display_id = None
    last_ads_list = []

    with open(submission_file, 'w') as submission_file:
        submission_file.write("display_id,ad_id\n")

        with gzip.open(test_data,'r') as test_data:
            with open(test_preds, 'r') as test_predictions:
                for rec in test_data:
                    split_rec = rec.decode().rstrip().split("|")
                    display_id = split_rec[display_id_col_idx].split(" ")[1].rstrip()
                    ad_id = split_rec[ad_id_col_idx].split(" ")[1].rstrip()
                    prediction = float(test_predictions.readline())

                    if display_id != last_display_id:
                        if last_display_id:
                            last_ads_list.sort(key=lambda x:x[1], reverse=True)
                            submission_file.write(last_display_id + "," + " ".join([x[0] for x in last_ads_list]) + "\n")
                        last_display_id = display_id
                        last_ads_list = [(ad_id, prediction)]
                    else:
                        last_ads_list.append((ad_id, prediction))

                last_ads_list.sort(key=lambda x:x[1], reverse=True)
                submission_file.write(last_display_id + "," + " ".join([x[0] for x in last_ads_list]) + "\n")

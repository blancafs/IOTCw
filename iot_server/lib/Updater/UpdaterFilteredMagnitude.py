import os, sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
sys.path.append(path+'/..')
print(path)

from helpers import *
from updater import Updater

class UpdaterFilteredMagnitude(Updater):
    def update(self, db):
        df = db

        xacc_df = pd.DataFrame(df['accel_x'], columns=['accel_x'])
        yacc_df = pd.DataFrame(df['accel_y'], columns=['accel_y'])
        zacc_df = pd.DataFrame(df['accel_z'], columns=['accel_z'])

        pd_merge = pd.concat([xacc_df, yacc_df, zacc_df], axis=1)
        pd_merge = pd_merge.values.tolist()

        d = {'mag_ax': []}
        mag_df = pd.DataFrame(data=d)
        i = 0
        for x, y, z in pd_merge:
            i += 1
            mag_df.loc[i] = math.sqrt(x * x + z * z + y * y)
        #     print(x,y,z)
        self.step_count = self.run(mag_df)

    def count_steps(self, my_data):
        lp_b, lp_a = get_low_pass_filter()
        my_data_filtered = np.array([filter_signal(lp_b, lp_a, my_signal) for my_signal in my_data.T])

        peaks, x = find_peaks(my_data_filtered[0], height=(None, None))
        troughs, y = find_peaks(-my_data_filtered[0], height=(None, None))

        peaks_coord = pd.Series(x['peak_heights'].tolist())

        troughs_coord = []
        for trough in troughs:
            troughs_coord.append(float(my_data_filtered[0].tolist()[trough]))  # pd.Series(y['peak_heights'].tolist())
        troughs_coord = pd.Series(troughs_coord)

        counter = 0
        for distance in abs(peaks_coord - troughs_coord):
            if distance > 0.05:
                counter += 1
        print(counter * 2)
        return counter * 2

    # For filtered use
    def run(self, data_frame, plot=False):
        df = data_frame#.copy()
        dim = [df.columns[0]]  # ['accel_z']#df.columns[0]#['accel_y']#['accel_x'] #data_frame[data_frame.columns[0]]
        steps = self.count_steps(df[dim].values)

        print("Steps for " + str(df.columns[0]) + ": " + str(steps))
        if (plot == True):
            plot_filter_vs_unfiltered(data_frame,
                                      dimensions_list=dim,
                                      data_points=200,
                                      color='red', min_max=True)
        return steps
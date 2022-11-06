package cn.fefu;

import com.github.sh0nk.matplotlib4j.Plot;
import com.github.sh0nk.matplotlib4j.PythonExecutionException;

import java.io.IOException;
import java.util.ArrayList;
import java.util.function.Function;

public class Main {
    private static final Integer COOLING = 0;
    private static final Integer HEATING = 1;
    private static final Integer T0 = 291;
    private static final Integer T_max = 483;
    private static final Integer T_min = 453;
    private static Integer state = HEATING;
    private static Integer thermostat(double T) {
        if (T >= T_max) {
            state = COOLING;
        } else if (T <= T_min) {
            state = HEATING;
        }
        return state.equals(COOLING) ? 0 : 1;
    }
    private static class Func implements Function<Double, Double> {
        @Override
        public Double apply(Double T) {
            double sigma = 5.67E-8;
            int P = 1600;
            int c = 900;
            double m = 0.8;
            double s = 0.01;
            int k = 25;
            return (P * thermostat(T)- k * s *(T - T0) - s * sigma *(Math.pow(T, 4) - Math.pow(T0, 4))) / (c * m);
        }
    }

    private static ArrayList<Double> euler(Function<Double, Double> func, ArrayList<Integer> t) {
        ArrayList<Double> res = new ArrayList<>();

        double T = T0.doubleValue();
        for (int tValue: t) {
            T += func.apply(T);
            res.add(T);
        }
        return res;
    }

    public static void main(String[] args) throws PythonExecutionException, IOException {
        ArrayList<Integer> t = new ArrayList<>();
        for(int i = 0; i <= 1500; ++i) {
            t.add(i);
        }

        ArrayList<Double> T = euler(new Func(), t);

        Plot plt = Plot.create();
        plt.plot().add(t, T);
        plt.xlabel("t");
        plt.ylabel("T");
        plt.savefig("fig8.svg");
        plt.show();
    }
}
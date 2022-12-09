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
    private static Integer state = HEATING;
    private static Integer thermostat(double T, double T_max, double T_min) {
        if (T >= T_max) {
            state = COOLING;
        } else if (T <= T_min) {
            state = HEATING;
        }
        return state.equals(COOLING) ? 0 : 1;
    }
    private static Double diffEq(Double T, int P, double c, double m, double S) {
        double sigma = 5.67E-8;
        int k = 25;
        return (P - k * S *(T - T0) - S * sigma *(Math.pow(T, 4) - Math.pow(T0, 4))) / (c * m);
    }

    private static Double diffEq(Double T, double T_max, double T_min, int P, double c, double m, double S) {
        double sigma = 5.67E-8;
        int k = 25;
        return (P * thermostat(T, T_max, T_min)- k * S *(T - T0) - S * sigma *(Math.pow(T, 4) - Math.pow(T0, 4))) / (c * m);
    }

    private static ArrayList<Double> euler(ArrayList<Integer> t, int P, double c, double m, double S) {
        ArrayList<Double> res = new ArrayList<>();

        double T = T0.doubleValue();
        for (int tValue: t) {
            T += diffEq(T, P, c, m, S);
            res.add(T-273);
        }
        return res;
    }

    private static ArrayList<Double> euler(ArrayList<Integer> t, double T_max, double T_min, int P, double c, double m, double S) {
        ArrayList<Double> res = new ArrayList<>();

        double T = T0.doubleValue();
        for (int tValue: t) {
            T += diffEq(T, T_max, T_min, P, c, m, S);
            res.add(T-273);
        }
        return res;
    }

    public static void main(String[] args) throws PythonExecutionException, IOException {
        ArrayList<Integer> t = new ArrayList<>();
        for(int i = 0; i <= 1500; ++i) {
            t.add(i);
        }

//        ArrayList<Double> T1 = euler(t, 493, 463,500, 530, 0.8, 0.02);
//        ArrayList<Double> T2 = euler(t, 443, 423,500, 530, 0.8, 0.02);

//        ArrayList<Double> T1 = euler(t, 493,463,500, 900, 0.8, 0.02);
//        ArrayList<Double> T2 = euler(t, 443, 423,500, 900, 0.8, 0.02);

//        ArrayList<Double> T1 = euler(t, 493, 463,500, 530, 0.8, 0.01);
//        ArrayList<Double> T2 = euler(t, 443, 423,500, 530, 0.8, 0.01);

//        ArrayList<Double> T1 = euler(t, 493, 463,500, 530, 1.0, 0.02);
//        ArrayList<Double> T2 = euler(t, 443, 423,500, 530, 1.0, 0.02);

        ArrayList<Double> T1 = euler(t,493,463, 700, 530, 0.8, 0.02);
        ArrayList<Double> T2 = euler(t,443,42   3, 700, 530, 0.8, 0.02);

        Plot plt = Plot.create();
        plt.plot().add(t, T1).label("T_max = 220");
        plt.plot().add(t, T2).label("T_max = 170");
        plt.xlabel("t");
        plt.ylabel("T");
        plt.legend();
        plt.savefig("fig6.svg");
        plt.show();
    }
}
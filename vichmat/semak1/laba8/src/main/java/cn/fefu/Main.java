package cn.fefu;

import org.apache.commons.math3.analysis.differentiation.DerivativeStructure;

import java.util.ArrayList;
import java.util.Arrays;

public class Main {
    private static double func(double x) {
        return 1.2*Math.pow(x, 2) - Math.sin(10*x);
    }

    private static double funcDerivative(double x, int order) {
        DerivativeStructure x_ = new DerivativeStructure(1, order+1, 0, x);
        DerivativeStructure res = ((x_.pow(2)).multiply(1.2)).subtract((x_.multiply(10)).sin());
        return res.getPartialDerivative(order);
    }

    private static ArrayList<ArrayList<Double>> getIntervals() {
        ArrayList<ArrayList<Double>> interval = new ArrayList<>();
        for(double a = 0; a < 1; a += .01) {
            if ((funcDerivative(a, 1)*funcDerivative(a+.01, 1) > 0)
                    && func(a)*func(a+.01) < 0
                    && funcDerivative(a, 2)*funcDerivative(a+.01, 2) > 0) {
                interval.add(new ArrayList<>(Arrays.asList(a, a+.01)));
            }
        }
        return interval;
    }

    private static void chordsAntTangent(ArrayList<Double> interval) {

        if (funcDerivative(interval.get(0), 2)*func(interval.get(0)) > 0) {
            double a = interval.get(0) - (func(interval.get(0)) / funcDerivative(interval.get(0), 1));
            double b = interval.get(1) - (func(interval.get(1)) * (interval.get(0) - interval.get(1))) /
                    (func(interval.get(0)) - func(interval.get(1)));
            interval.set(0, a);
            interval.set(1, b);
        } else {
            double b = interval.get(1) - (func(interval.get(1)) / funcDerivative(interval.get(1), 1));
            double a = interval.get(0) - (func(interval.get(0)) * (interval.get(1) - interval.get(0))) /
                    (func(interval.get(1)) - func(interval.get(0)));
            interval.set(0, a);
            interval.set(1, b);
        }
    }

    public static void main(String[] args) {
        double epsilon = 10E-6;
        ArrayList<ArrayList<Double>> intervals = getIntervals();
        for (ArrayList<Double> interval: intervals) {
            while (Math.abs(interval.get(0) - interval.get(1)) > epsilon) {
                chordsAntTangent(interval);
            }
            System.out.printf("x = %.6f\n", (interval.get(1) + interval.get(0)) / 2);
        }
    }
}
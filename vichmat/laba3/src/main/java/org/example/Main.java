package org.example;

import org.apache.commons.math3.analysis.differentiation.DerivativeStructure;
import org.apache.commons.math3.util.CombinatoricsUtils;

import java.util.*;
import java.util.function.Function;

public class Main {
    private final static Double a = 0.4;

    private final static Double b = 0.9;

    private final static Double h = (b - a) / 10;

    private static final ArrayList<Double> xs = new ArrayList<>() {{
        add(0.42);
        add(0.87);
        add(0.67);
    }};

    private static class Func implements Function<Double, Double> {

        @Override
        public Double apply(Double x) {
            return Math.pow(x, 2) + Math.log(x);
        }
    }

    private static ArrayList<Double> getGrid() {
        ArrayList<Double> grid = new ArrayList<>();
        for(int i = 0; i <= 10; ++i) {
            grid.add(a + i * h);
        }
        return grid;
    }

    private static Double finiteDifference(Function<Double, Double> func, Integer order,
                                           Double x0, Double idx) {
        if (order == 0) {
            return func.apply(x0 + h * idx);
        }
        return finiteDifference(func, order - 1, x0, idx + 0.5) -
                finiteDifference(func, order - 1, x0, idx - 0.5);
    }

    private static Double newton1(Function<Double, Double> func, ArrayList<Double> grid,
                                 Double x) {
        double x0 = grid.get(0);
        double t = (x - x0) / h;
        double num = 1.;
        double res = func.apply(x0);
        for(int i = 1; i < grid.size(); i++) {
           num *= (t - (i - 1));
           res += num * finiteDifference(func, i, x0, i/(double)2) / CombinatoricsUtils.factorial(i);
        }
        return res;
    }

    private static Double newton2(Function<Double, Double> func, ArrayList<Double> grid,
                                  Double x) {
        double x0 = grid.get(grid.size()-1);
        double t = (x - x0) / h;
        double num = 1.;
        double res = func.apply(x0);
        for(int i = 1; i < grid.size(); i++) {
            num *= (t + (i - 1));
            res += num * finiteDifference(func, i, x0, -i/(double)2) / CombinatoricsUtils.factorial(i);
        }
        return res;
    }

    private static Double gauss1(Function<Double, Double> func, ArrayList<Double> grid,
                                 Double x) {
        double x0 = 0;
        double t = 0;
        double res = 0;
        int n = grid.size() - 1;
        for(int i = 0; i < grid.size(); ++i) {
            if (grid.get(i) > x) {
                x0 = grid.get(i-1);
                t = (x - x0) / h;
                res = func.apply(x0);
                break;
            }
        }

        double num = 1.;
        for(int i = 1; i <= n/2; ++i) {
            num *= t + i - 1;
            res += num * finiteDifference(func, 2*i-1, x0, 0.5) / CombinatoricsUtils.factorial(2 * i - 1);
            num *= t - i;
            res += num * finiteDifference(func, 2*i, x0, 0.) / CombinatoricsUtils.factorial(2 * i);
        }
        return res;
    }

    private static ArrayList<Double> remainder(ArrayList<Double> grid, Double xToFind) {
        ArrayList<Double> res = new ArrayList<>();
        for (double gridX: grid) {
            DerivativeStructure x_ = new DerivativeStructure(1, 11, 0, gridX);
            DerivativeStructure der11 = x_.pow(2).add(x_.log());
            double w = 1.;
            for(double x: grid) {
                w *= xToFind - x;
            }
            res.add(Math.abs(der11.getPartialDerivative(11) * w / CombinatoricsUtils.factorial(11)));
        }
        return res;
    }

    private static ArrayList<Double> derivatives(ArrayList<Double> grid) {
        ArrayList<Double> res = new ArrayList<>();
        for (double gridX: grid) {
            DerivativeStructure x_ = new DerivativeStructure(1, 11, 0, gridX);
            DerivativeStructure der11 = x_.pow(2).add(x_.log());
            res.add(der11.getPartialDerivative(11));
        }
        return res;
    }

    public static void main(String[] args) {
        ArrayList<Double> grid = getGrid();

        System.out.println("\n---------x**(newton 1)---------");
        Double newton1 = newton1(new Func(), grid, xs.get(0));
        System.out.println("newton1(x**) - f(x**) = " + Math.abs(newton1 - new Func().apply(xs.get(0))));
        System.out.println("Max R = " + Math.abs(Collections.max(remainder(grid, xs.get(0)))));
        System.out.println("Min R = " + Math.abs(Collections.min(remainder(grid, xs.get(0)))));


        System.out.println("\n---------x***(newton 2)---------");
        Double newton2 = newton2(new Func(), grid, xs.get(1));
        System.out.println("newton2(x***) - f(x***) = " + Math.abs(newton2 - new Func().apply(xs.get(1))));
        System.out.println("Max R = " + Collections.max(remainder(grid, xs.get(1))));
        System.out.println("Min R = " + Collections.min(remainder(grid, xs.get(1))));


        System.out.println("\n---------x****(gauss 1)---------");
        Double gauss1 = gauss1(new Func(), grid, xs.get(2));
        System.out.println("gauss1(x****) - f(x****) = " + Math.abs(gauss1 - new Func().apply(xs.get(2))));
        System.out.println("Max R = " + Collections.max(remainder(grid, xs.get(2))));
        System.out.println("Min R = " + Collections.min(remainder(grid, xs.get(2))));


        System.out.println("\n---------derivatives---------");
        System.out.println("Max 11 derivative = " + Collections.max(derivatives(grid)));
        System.out.println("Min 11 derivative = " + Collections.min(derivatives(grid)));
    }
}

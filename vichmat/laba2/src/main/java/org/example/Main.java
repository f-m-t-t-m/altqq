package org.example;

import java.util.*;
import java.util.function.*;

import org.apache.commons.math3.util.*;

public class Main {

    public static class Func implements Function<Double, Double> {

        @Override
        public Double apply(Double x) {
            return Math.pow(x, 2) + Math.log(x);
        }

    }

    public static class FuncDerivativeSecondOrder implements Function<Double, Double> {

        @Override
        public Double apply(Double x) {
            return 2 - Math.pow(x, -2);
        }

    }

    public static class FuncDerivativeThirdOrder implements Function<Double, Double> {

        @Override
        public Double apply(Double x) {
            return -6 * Math.pow(x, -4);
        }

    }
    static double a = 0.4;
    static double b = 0.9;

    public static ArrayList<Double> getGrid(double a, double b, int N) {
        ArrayList<Double> grid = new ArrayList<>();
        double h = (b - a) / N;
        for(int i = 0; i <= N; i++) {
            grid.add(a + i * h);
        }

        return grid;
    }

    public static double divDiff(ArrayList<Double> xs, int start, int end, Function<Double, Double> func) {
        if (start == end) {
            return func.apply(xs.get(start));
        }
        double divFirst = divDiff(xs, start + 1, end, func);
        double divSecond = divDiff(xs, start, end - 1, func);
        return (divFirst - divSecond)/(xs.get(end) - xs.get(start));
    }

    public static ArrayList<Double> findNClosestValues(ArrayList<Double> grid, double x, int count) {
        ArrayList<Double> xs = new ArrayList<>();

        for(int i = 1; i < grid.size(); i++) {
            if (grid.get(i) > x) {
                int l = i - 2;
                int r = i + 1;
                xs.add(grid.get(i-1));
                xs.add(grid.get(i));
                while (xs.size() != count && (l >= 0 || r <= grid.size() - 1)) {
                    if ( l < 0 && r <= grid.size() - 1) {
                        xs.add(grid.get(r++));
                    } else if ( l >= 0 && r > grid.size() - 1) {
                        xs.add(0, grid.get(l--));
                    } else {
                        if (Math.abs(grid.get(l) - x) < Math.abs(grid.get(r) - x)) {
                            xs.add(0, grid.get(l--));
                        }
                        else {
                            xs.add(grid.get(r++));
                        }
                    }
                }
                break;
            }
        }
        return xs;
    }

    public static ArrayList<Double> getRs(ArrayList<Double> xs, double x, Function<Double, Double> derivative) {
        ArrayList<Double> rs = new ArrayList<>();
        double ans = .0;
        for(double xValue: xs) {
            ans = derivative.apply(xValue);
            for (double xValue2: xs) {
                ans *= (x - xValue2);
            }
            rs.add(Math.abs(ans / CombinatoricsUtils.factorial(xs.size())));
        }

        return rs;
    }

    public static double newtonFirstOrder(ArrayList<Double> grid, Double x,
                                        Function<Double, Double> func) {
        ArrayList<Double> xs = findNClosestValues(grid, x, 2);
        double ans = func.apply(xs.get(0)) + divDiff(xs, 0, 1, func)*(x - xs.get(0));
        System.out.println("N_1 = " + ans);
        return ans;
    }

    public static double newtonSecondOrder(ArrayList<Double> grid, Double x,
                                        Function<Double, Double> func) {
        ArrayList<Double> xs = findNClosestValues(grid, x, 3);
        double ans = func.apply(xs.get(0)) + divDiff(xs, 0, 1, func)*(x - xs.get(0))
                     + divDiff(xs, 0, 2, func) * (x-xs.get(0)) * (x - xs.get(1));
        System.out.println("N_2 = " + ans);
        return ans;
    }

    public static Double lagrange(ArrayList<Double> grid, Double x,
                                  Function<Double, Double> func, int order,
                                  Function<Double, Double> derivative) {
        ArrayList<Double> xs = findNClosestValues(grid, x, order + 1);
        double ans = 0;
        for (Double xValue: xs) {
            double localAns = func.apply(xValue);
            for(Double xValue2: xs) {
                if (!xValue.equals(xValue2)) {
                    localAns *= (x - xValue2);
                    localAns /= (xValue - xValue2);
                }
            }
            ans += localAns;
        }

        ArrayList<Double> rs = getRs(xs, x, derivative);
        Collections.sort(rs);
        System.out.println("min R = " + rs.get(0));
        System.out.println("max R = " + rs.get(rs.size() - 1));
        System.out.println("L(x) - f(x) = " + Math.abs(ans - func.apply(x)));
        System.out.println("L(x) = " + ans);
        return ans;
    }

    public static void main(String[] args) {
        ArrayList<Double> grid = getGrid(a, b, 10);

        System.out.println("\n------------Lagrange First Order------------");
        double lfo = lagrange(grid, 0.52, new Func(),1, new FuncDerivativeSecondOrder());

        System.out.println("\n------------Lagrange Second Order------------");
        double lso = lagrange(grid, 0.52, new Func(),2, new FuncDerivativeThirdOrder());

        System.out.println("\n------------Newton First Order------------");
        double nfo = newtonFirstOrder(grid, 0.43, new Func());
        System.out.println("N_1 - L_1 = " + (lfo - nfo));

        System.out.println("\n------------Newton Second Order------------");
        double nso =newtonSecondOrder(grid, 0.43, new Func());
        System.out.println("N_2 - L_2 = " + (lso - nso));
    }

}

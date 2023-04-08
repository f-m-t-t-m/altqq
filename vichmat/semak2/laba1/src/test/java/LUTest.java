import org.example.LUDecomposition;
import org.example.MatrixUtils;
import org.junit.jupiter.api.Test;

import java.util.Arrays;

public class LUTest {

    final double[][] a = {
            {0.416, 3.273, 0.326, 0.375},
            {0.297, 0.351, 2.997, 0.429},
            {0.412, 0.194, 0.215, 3.628},
            {4.003, 0.207, 0.519, 0.281}
    };

    @Test
    void testLUDecompose() {
        LUDecomposition decomposition = new LUDecomposition(a);
        double[][] r = MatrixUtils.multiply(decomposition.getL(), decomposition.getU());
        MatrixUtils.printMatrix(r);
    }

}

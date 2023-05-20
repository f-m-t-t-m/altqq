import org.example.MatrixUtils;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class MatrixUtilsTest {
    @Test
    void test_that_matrix_is_triangular() {
        double[][] a = {{1, 2, 3},
                        {0, 4, 5},
                        {0, 0, 6}};
        assertTrue(MatrixUtils.isMatrixTriangular(a));
    }

    @Test
    void test_that_matrix_is_not_triangular() {
        double[][] a = {{1, 2, 3},
                        {0, 4, 5},
                        {0, 1, 6}};
        assertFalse(MatrixUtils.isMatrixTriangular(a));
    }

}

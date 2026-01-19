#ifndef IO_GENERATOR_H
#define IO_GENERATOR_H
extern const int PI_WIDTH = 1;
extern const int LATCH_WIDTH = 1;
extern const int PO_WIDTH = 1;
void io_generator(bool* pi, bool* li, bool* po, bool* lo) {
    bool n0 = false;
    bool n1 = pi[0];
    bool n2 = li[0];
    bool n3 = n2 && n1;
    bool n4 = !n2 && !n1;
    bool n5 = !n4 && !n3;
    lo[0] = !n5;
    po[0] = n2;
}
#endif
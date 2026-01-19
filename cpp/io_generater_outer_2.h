#ifndef IO_GENERATOR_H
#define IO_GENERATOR_H
extern const int PI_WIDTH = 1;
extern const int LATCH_WIDTH = 2;
extern const int PO_WIDTH = 1;
void io_generator(bool* pi, bool* li, bool* po, bool* lo) {
    bool n0 = false;
    bool n1 = pi[0];
    bool n2 = li[0];
    bool n3 = li[1];
    bool n4 = n3 && n1;
    bool n5 = !n3 && !n1;
    bool n6 = !n5 && !n4;
    bool n7 = n3 && n1;
    bool n8 = !n3 && !n1;
    bool n9 = !n8 && !n7;
    lo[0] = !n6;
    lo[1] = n9;
    po[0] = n2;
}
#endif
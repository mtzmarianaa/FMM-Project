/*
General methods for dealing with txt files, specially ints or doubles separated by commas
*/
#pragma once

void separateARowInt(char *line, int nElementsRow, int *row);

void separateARowDb(char *line, int nElementsRow, double *row);

int numberElementsInRow(char *line, int nCharInLine);

int numLinesInFile(const char *pathFile);

void readIntColumn(const char *pathFile, int *column);

void saveTimes(double times[5], const char *pathFile);
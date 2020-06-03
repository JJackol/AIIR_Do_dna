// ./main <input_file> <substring_length> <output_file>
#include <cstdint>
#include <exception>
#include <fstream>
#include <functional>
#include <iostream>
#include <iterator>
#include <math.h>
#include <optional>
#include <random>
#include <regex>
#include <string>

int main(int argc, char *argv[])
{

  std::default_random_engine generator;
  std::uniform_int_distribution<int> distribution(1,4);

  auto getNucleotide = [&generator, &distribution] ()
  {
    switch (distribution(generator))
    {
      case 1: return 'A';
      case 2: return 'T';
      case 3: return 'C';
      case 4: return 'G';
    }
    return 'X';
  };

  auto isNucleotide = [] (std::string s) { return std::regex_match(s, std::regex("[ATCG]+")); };

  auto sizeofFile = [] (std::ifstream& in) { auto size = in.tellg(); in.seekg(0); return size; };

  auto generateFileWithNucleotides = [&getNucleotide] (uint64_t N, std::string filename)
  {
    std::ofstream ofs (filename, std::ofstream::out);
    for (size_t i = 0; i < N; i++)
    {
      ofs << getNucleotide();
    }
    ofs.close();
  };

  //generateFileWithNucleotides(950, "950.txt");

  if(argc != 4)
  {
    std::cout << "Unexpected number of args" << std::endl;
    std::terminate();
  }

  std::string filename(argv[1]);
  std::string lengthOfSubstringString(argv[2]);
  std::string outputFilename(argv[3]);

  auto lengthOfSubstring = std::stoi(lengthOfSubstringString);

  if(std::ifstream inStream{filename, std::ios::binary | std::ios::ate})
  {
    auto size = sizeofFile(inStream);

    // N = ceil(S/L*0.5)
    // for S(100) and L(15) = 4
    // step = S/N =

    auto iterator = 0;
    auto overflowFlag = false;
    char charBuffer;
    uint64_t N = ceil((float)size/lengthOfSubstring*0.5);
    uint64_t step = ceil(size/N);

    std::cout << std::endl << "File size: " << size << std::endl;
    std::cout << "Output filename: " << outputFilename << std::endl;
    std::cout << "Substr. len: " << lengthOfSubstring << std::endl;
    std::cout << "Calculated parts number: " << N << std::endl;
    std::cout << "Calculated raw step: " << step << std::endl;
    std::cout << "Calculated overlay step: " << step+lengthOfSubstring << std::endl;

    while(true)
    {
      uint64_t p = iterator;
      uint64_t q = iterator+step+lengthOfSubstring-1;
      if(q>size) { q=size; overflowFlag=true; }

      inStream.seekg(p);
      std::string filename = outputFilename + "_" + std::to_string(p) + "_" + std::to_string(q);
      std::ofstream outfs (filename, std::ofstream::out);
      for (size_t j = p; j <= q; j++)
      {
        inStream.get(charBuffer);
        outfs << charBuffer;
      }
      outfs.close();

      if(overflowFlag) break;

      iterator += step;
    }
  }
  else
  {
    std::cout << "Failed to open " << filename << std::endl;
    std::terminate();
  }

  std::cout << std::endl;

  return 0;
}

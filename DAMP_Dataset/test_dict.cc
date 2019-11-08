#include <iostream>
#include <map>
#include <string>
#include <stdio.h>

using namespace std;

int main(void)
{
    typedef map<string, string> my_diction;
    my_diction diction;

    for (int i = 0; i<10; i++)
    {
        // string name
        std::string key;
        key.assign("example");
        key.append(to_string(i));
        std::string value;
        value.assign(to_string(i));
        // char value[strlen("%d")];
        // sprintf(value,"%d",i);
        diction[key] = value;

    }

    my_diction::iterator dict_iter;

    for (dict_iter = diction.begin(); dict_iter!=diction.end(); ++dict_iter)
    {
        cout<<dict_iter->first<<" : "<<dict_iter->second<<"\n";


    }

    return 1;
}
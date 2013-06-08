-module(asntest).
-compile(export_all).


    
%% PDU ONE CHOICE
ebinary_modTest_choiceOne() ->
    Msg         = {choiceOne, "AB"},
    {ok, Bin}   = 'ModTest':encode('TestPDU', Msg),
    {ok, Msg}   = 'ModTest':decode('TestPDU', Bin),
    ok          = file:write_file("ebinary_modTest_choiceOne.bin", Bin).
ebinary_modTest_choiceOne(String) ->
    Msg         = {choiceOne, String},
    {ok, Bin}   = 'ModTest':encode('TestPDU', Msg),
    {ok, Msg}   = 'ModTest':decode('TestPDU', Bin),
    ok          = file:write_file("ebinary_modTest_choiceOne.bin", Bin).

ebinary_modTest_choiceTwo() ->
    Msg         = {choiceTwo, "AB"},
    {ok, Bin}   = 'ModTest':encode('TestPDU', Msg),
    {ok, Msg}   = 'ModTest':decode('TestPDU', Bin),
    ok          = file:write_file("ebinary_modTest_choiceTwo.bin", Bin).
ebinary_modTest_choiceTwo(String) ->
    Msg         = {choiceTwo, String},
    {ok, Bin}   = 'ModTest':encode('TestPDU', Msg),
    {ok, Msg}   = 'ModTest':decode('TestPDU', Bin),
    ok          = file:write_file("ebinary_modTest_choiceTwo.bin", Bin).

%% PDU TWO CHOICES
ebinary_NmsPDU_modTest_choiceTwo() ->
    Msg         = {modTest, {choiceTwo, "AB"}},
    {ok, Bin}   = 'NmsPDU':encode('PDU', Msg),
    {ok, Msg}   = 'NmsPDU':decode('PDU', Bin),
    ok          = file:write_file("ebinary_NmsPDU_modTest_choiceTwo.bin", Bin).
ebinary_NmsPDU_modTest_choiceTwo(String) ->
    Msg         = {modTest, {choiceTwo, String}},
    {ok, Bin}   = 'NmsPDU':encode('PDU', Msg),
    {ok, Msg}   = 'NmsPDU':decode('PDU', Bin),
    ok          = file:write_file("ebinary_NmsPDU_modTest_choiceTwo.bin", Bin).

ebinary_NmsPDU_modTest_choiceOne() ->
    Msg         = {modTest, {choiceOne, "AB"}},
    {ok, Bin}   = 'NmsPDU':encode('PDU', Msg),
    {ok, Msg}   = 'NmsPDU':decode('PDU', Bin),
    ok          = file:write_file("ebinary_NmsPDU_modTest_choiceOne.bin", Bin).
ebinary_NmsPDU_modTest_choiceOne(String) ->
    Msg         = {modTest, {choiceOne, String}},
    {ok, Bin}   = 'NmsPDU':encode('PDU', Msg),
    {ok, Msg}   = 'NmsPDU':decode('PDU', Bin),
    ok          = file:write_file("ebinary_NmsPDU_modTest_choiceOne.bin", Bin).

%% Generated by the Erlang ASN.1 BER_V2-compiler version, utilizing bit-syntax:1.8
%% Purpose: encoder and decoder to the types in mod ModTest

-module('ModTest').
-define('RT_BER',asn1rt_ber_bin_v2).
-asn1_info([{vsn,'1.8'},
            {module,'ModTest'},
            {options,[ber_bin_v2,warnings,errors,{cwd,[47,104,111,109,101,47,115,101,98,47,115,114,99,47,116,107,111,114,100,101,114,45,113,116,45,48,46,49,46,48,47,116,101,115,116,47,97,115,110,49]},{outdir,[47,104,111,109,101,47,115,101,98,47,115,114,99,47,116,107,111,114,100,101,114,45,113,116,45,48,46,49,46,48,47,116,101,115,116,47,97,115,110,49]},nif,optimize,warnings_as_errors,{i,[46]},{i,[47,104,111,109,101,47,115,101,98,47,115,114,99,47,116,107,111,114,100,101,114,45,113,116,45,48,46,49,46,48,47,116,101,115,116,47,97,115,110,49]}]}]).

-export([encoding_rule/0]).
-export([
'enc_TestPDU'/2
]).

-export([
'dec_TestPDU'/2
]).

-export([info/0]).


-export([encode/2,decode/2,encode_disp/2,decode_disp/2]).

encoding_rule() ->
   ber_bin_v2.

encode(Type,Data) ->
case catch encode_disp(Type,Data) of
  {'EXIT',{error,Reason}} ->
    {error,Reason};
  {'EXIT',Reason} ->
    {error,{asn1,Reason}};
  {Bytes,_Len} ->
    {ok,Bytes};
  Bytes ->
    {ok,Bytes}
end.

decode(Type,Data) ->
case catch decode_disp(Type,element(1,?RT_BER:decode(Data,nif))
) of
  {'EXIT',{error,Reason}} ->
    {error,Reason};
  {'EXIT',Reason} ->
    {error,{asn1,Reason}};
  Result ->
    {ok,Result}
end.

encode_disp('TestPDU',Data) -> 'enc_TestPDU'(Data);
encode_disp(Type,_Data) -> exit({error,{asn1,{undefined_type,Type}}}).


decode_disp('TestPDU',Data) -> 'dec_TestPDU'(Data);
decode_disp(Type,_Data) -> exit({error,{asn1,{undefined_type,Type}}}).





info() ->
   case ?MODULE:module_info() of
      MI when is_list(MI) ->
         case lists:keysearch(attributes,1,MI) of
            {value,{_,Attributes}} when is_list(Attributes) ->
               case lists:keysearch(asn1_info,1,Attributes) of
                  {value,{_,Info}} when is_list(Info) ->
                     Info;
                  _ ->
                     []
               end;
            _ ->
               []
         end
   end.


%%================================
%%  TestPDU
%%================================
'enc_TestPDU'(Val) ->
    'enc_TestPDU'(Val, []).


'enc_TestPDU'({'TestPDU',Val}, TagIn) ->
   'enc_TestPDU'(Val, TagIn);

'enc_TestPDU'(Val, TagIn) ->
   {EncBytes,EncLen} = case element(1,Val) of
      choiceOne ->
         ?RT_BER:encode_restricted_string([], element(2,Val), 19, [<<129>>]);
      choiceTwo ->
         ?RT_BER:encode_restricted_string([], element(2,Val), 19, [<<130>>]);
      Else -> 
         exit({error,{asn1,{invalid_choice_type,Else}}})
   end,

?RT_BER:encode_tags(TagIn, EncBytes, EncLen).




'dec_TestPDU'(Tlv) ->
   'dec_TestPDU'(Tlv, []).

'dec_TestPDU'(Tlv, TagIn) ->
Tlv1 = ?RT_BER:match_tags(Tlv,TagIn), 
case (case Tlv1 of [CtempTlv1] -> CtempTlv1; _ -> Tlv1 end) of

%% 'choiceOne'
    {131073, V1} -> 
        {choiceOne, ?RT_BER:decode_restricted_string(V1,[],19,[])};


%% 'choiceTwo'
    {131074, V1} -> 
        {choiceTwo, ?RT_BER:decode_restricted_string(V1,[],19,[])};

      Else -> 
         exit({error,{asn1,{invalid_choice_tag,Else}}})
   end
.

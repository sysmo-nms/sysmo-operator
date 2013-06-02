% depuis "make start" de "nms_project",
AsnPdu = {modTrackerPDU,
        {fromServer,
            {cmdResp,
                {'CommandResponce',
                    666,
                    "number of the beast"
    }   }   }   }.

% write to file
{ok, B}  = 'NmsPDU':encode('PDU', AsnPdu).
ok       = file:write_file("pdu.bin", B).

% extract from file
{ok, Bin} = file:read_file("pdu.bin").
{ok, Rep} = 'NmsPDU':decode('PDU', Bin).

Rep = AsnPdu.

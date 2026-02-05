# Ground Truth Answers

TLDR: Scroll to find the "correct" Yes/No/Uncertain answers to the questionnare

## Process

I generated this truth table using **NotebookLM** to serve as a reliable benchmark for my implementation. I used my Google AI Pro student subscription (increases max sources/notebook from 100->300). Then, I utilized the tool's RAG capabilities for high-accuracy verification (because it's supposedly the best consumer one out there, plus I use it for school).

- **Partitioning:** Due to the 300-page limit per notebook, I split the source documents across two separate notebooks (1 299-sources, 1 73-sources)
- **Batching:** To accommodate token limits, I processed the questions in small batches
- **Consolidation:** The final results below combine the outputs from both notebooks to ensure complete coverage and correct answers

## Output

```
Final Summary Counts

Total Questions: 64

YES: 26

NO: 38

UNCERTAIN: 0
```

```
Detailed Questionnaire Responses

1. Does the P&P state that under existing Contract requirements and state law, MCPs are required to provide hospice services upon Member election...?

Answer: YES

Source: GG.1503, Pages 1-2, Sections II.A and II.D

2. Does the P&P state that Members who qualify for and elect to receive hospice care services remain enrolled in an MCP while receiving such services?

Answer: YES

Source: GG.1503, Page 2, Sections II.A and II.L

3. Does the P&P state that to avoid problems caused by late referrals, MCP P&Ps should clarify... how Members may access hospice care services... preferably within 24 hours...?

Answer: YES

Source: GG.1503, Page 3, Section II.F.3

4. Does the P&P state MCPs may restrict coverage to in-Network Providers, unless Medically Necessary services are not available in-Network...?

Answer: YES

Source: GG.1539, Page 2, Section II.A

5. Does the P&P state Members who elect hospice care are entitled to curative treatment for conditions unrelated to their terminal illness?

Answer: YES

Source: GG.1503, Pages 2 and 6, Sections II.C.4, II.L, and II.M

6. Does the P&P state that for out-of-Network hospice Providers, the MCP should seek an agreement, such as a single case agreement...?

Answer: YES

Source: EE.1141, Pages 2-3; GG.1503, Page 3

7. Does the P&P state that while Prior Authorization for hospice services is restricted... MCPs are required to review documentation to avoid Fraud, Waste, and Abuse?

Answer: NO

Reasoning: Policy restricts PA but does not explicitly link it to FWA reviews in this specific context.

8. Does the P&P state that to avoid possible delays... MCP P&Ps should clarify... how Members may access hospice care services... after the MCP confirms qualifications...?

Answer: NO

9. Does the P&P state that for out-of-Network hospice Providers, MCPs must ensure the hospice Provider has Medicare certification, is licensed by CDPH, and has an NPI...?

Answer: NO

10. Does the P&P state that requirements for the initiation of outpatient hospice services include a certification by the attending physician and/or the hospice medical director...?

Answer: YES

Source: GG.1503, Page 2, Section II.C

11. Does the P&P state that election of hospice care occurs when the Member... files an election statement... and the hospice Provider must submit the... DHCS election form... within five calendar days...?

Answer: NO

Reasoning: Policy timeline (30 days) does not match the APL requirement (5 days).

12. Does the P&P state that in instances where the hospice Provider does not timely submit the election form... the MCP is not obligated to cover and pay... and the hospice Provider cannot bill the Member?

Answer: NO

13. Does the P&P state DHCS and MCPs may conduct medical and site reviews... regarding a Member's certification and election?

Answer: NO

14. Does the P&P state that a hospice Provider must obtain written certification of terminal illness for each hospice benefit period? (Includes detailed certifier list)

Answer: NO

15. Does the P&P state that "terminally ill" means that an individual has a medical prognosis that their life expectancy is six months or less...?

Answer: YES

Source: GG.1503, Pages 2, 8, 10, 18

16. Does the P&P state MCPs must not deny hospice care to Members certified as terminally ill?

Answer: YES

Source: GG.1503, Pages 1 and 8, Sections II.A and III.A

17. Does the P&P state guidance provided by CMS... is not wholly restrictive... and do not replace a physician's professional judgement?

Answer: NO

18. Does the P&P state only general inpatient care is subject to Prior Authorization... and that the five listed documents must be submitted...?

Answer: NO

Reasoning: Document requirements in Policy differ from the list of five in the question.

19. Does the P&P state hospices must notify the MCP of general inpatient care placements that occur after normal business hours on the next business day?

Answer: NO

20. Does the P&P state an MCP may require documentation of medical justification for continuous home care and/or respite home care... and reimbursement may be reduced...?

Answer: NO

21. Does the P&P state payment... may be denied if it is determined... that the hospice care services are not medically necessary... with liability placed on the hospice Provider?

Answer: NO

22. Does the P&P state MCP procedures must facilitate Member election... by engaging in practices that avoid unnecessary delays... and prevent Fraud, Waste, and Abuse?

Answer: NO

23. Does the P&P state the Member's election of hospice care services must include the five listed elements on the appropriate DHCS hospice election form?

Answer: NO

Reasoning: Policy lists four elements, not five.

24. Does the P&P state a Member may elect to receive hospice care during one or more of the following periods: (1) 90-day; (2) 90-day; (3) unlimited 60-day?

Answer: YES

Source: GG.1503, Page 2, Section II.D

25. Does the P&P state that upon Member election... MCPs must ensure provision of, and payment for, the 12 listed hospice care services... and may require in-Network Provider use?

Answer: YES

Source: GG.1503, Pages 1-2, 16-17; GG.1539, Page 2

26. Does the P&P further state physician services include: (1) general supervisory services... (2) participation in establishment of plans of care...?

Answer: NO

Reasoning: Specific definitions and billing instructions not explicitly found.

27. Does the P&P state a Member's voluntary election may be revoked... and the hospice Provider must submit the... statement... within five calendar days...?

Answer: NO

Reasoning: 5-day deadline and retroactive prohibition clause not found.

28. Does the P&P state that at any time after revocation... a Member may execute a new election... and the benefit periods of care restart?

Answer: NO

29. Does the P&P state that if the Member re-elects hospice care, the hospice Provider must submit a new hospice election form...?

Answer: NO

30. Does the P&P state a Member... may change the designation of a hospice Provider once in each benefit period... and this is not a revocation?

Answer: NO

Reasoning: Policy limits change to "once per election period" only when moving out of county.

31. Does the P&P include the four listed special considerations in hospice election MCPs are required or expected to adhere to?

Answer: NO

32. Does the P&P include the face-to-face encounter requirements and criteria?

Answer: YES

Source: GG.1503, Page 10, Sections III.F.4.a, III.F.5, III.F.6, and III.F.7

33. Does the P&P state MCPs must instruct staff... of the importance of timely recognition... and facilitate the transfer of services...?

Answer: NO

34. Does the P&P state under EPSDT, children... may receive additional services... (Concurrent Care)?

Answer: YES

Source: GG.1503, Page 2; GG.1550, Page 2

35. Does the P&P state hospice and palliative care is available for CCS eligible children... and MCPs should contact their respective CCS county office...?

Answer: YES

Source: GG.1503, Pages 2 and 8; GG.1550, Pages 6 and 11; GG.1101, Pages 2, 7, 9

36. Does the P&P state that Under section 2302 of the ACA... Medicaid children... may continue to receive services to treat their terminal illness?

Answer: YES

Source: GG.1503, Page 2; GG.1550, Pages 11-12

37. Does the P&P state that due to the highly specialized services... federal law mandates that the hospice designate an interdisciplinary group(s)...?

Answer: NO

38. Does the P&P state Medi-Cal program payments... are based upon the level of care... and MCPs must update their rates annually...?

Answer: NO

39. Does the P&P state MCPs may pay more, but not less than, the Medicare rate... and include the seven listed revenue codes?

Answer: NO

40. Does the P&P state a hospice day billed at the routine home care level in the first 60 days... is paid at the high rate... and day 61 or later at the low rate?

Answer: YES

Source: GG.1503, Pages 4 and 6, Sections II.F.5 and II.J

41. Does the P&P state MCPs must pay inpatient rates... except the day on which a Member is discharged?

Answer: NO

42. Does the P&P state that... hospice services are Covered Services and are not categorized as Long-Term Care (LTC) services...?

Answer: NO

43. Does the P&P state MCPs cannot require authorization for room and board for Members receiving hospice services and residing in a SNF/NF...?

Answer: NO

Reasoning: Policy requires "Notification" which technically differs from "Cannot require authorization" in this legal context.

44. Does the P&P state a Member who is a resident of a SNF or ICF may elect hospice care, and that payment... will be provided to the hospice...?

Answer: YES

Source: GG.1503, Pages 2 and 6, Sections II.A.3 and II.I

45. Does the P&P state the hospice Provider must reimburse the facility for the room and board at the rate negotiated... (95% rule)?

Answer: NO

46. Does the P&P state LTC Members who elect the Medi-Cal hospice benefit are not disenrolled from the MCP, and that hospices will bill the MCPs using the six listed revenue codes?

Answer: NO

47. Does the P&P state that for all Members with both Medicare and Medi-Cal coverage (dual eligibles), MCPs must ensure that Medicare remains the primary payor...?

Answer: YES

Source: FF.2003, Pages 10-12; GG.1503, Pages 2 and 6

48. Does the P&P state that for dually eligible SNF residents... payment for room and board must be made directly to the hospice Provider?

Answer: NO

49. Does the P&P state MCPs cannot require authorization for the hospice Provider to bill the MCP for the room and board... while the patient is receiving hospice services under Medicare?

Answer: NO

50. Does the P&P state the hospice Provider must submit the DHCS election form to both DHCS and the Member's respective MCP... for dual eligibles...?

Answer: NO

Reasoning: Policy states dual eligibles in the community are exempt from notification.

51. Does the P&P state the MCP will then pay the room and board payment to the hospice Provider... and the hospice must be responsible for paying the nursing home?

Answer: NO

52. Does the P&P state that if hospice services... are covered by a recipient's Other Health Coverage insurance, MCPs must ensure hospice Providers bill the Other Health Coverage prior to billing Medi-Cal...?

Answer: YES

Source: FF.2003, Pages 2-3, 12-13; GG.1503, Page 2

53. Does the P&P state hospice Providers must use Revenue Code 0657 when billing for physician services... limited to one visit-per-day...?

Answer: YES

Source: GG.1503, Page 6, Section II.K; Page 18

54. Does the P&P state that consulting/special physician services Revenue Code 0657 may be billed only for physician services to manage symptoms that cannot be remedied by the Member's attending physician...?

Answer: YES

Source: GG.1503, Page 18, Section IX

55. Does the P&P state that the Medi-Cal Fee-For-Service (FFS) program does not permit Prior Authorization of hospice services... therefore, MCPs adhere to the same Utilization Review standards...?

Answer: YES

Source: GG.1503, Pages 3-4, Sections II.F.3 and II.F.4

56. Does the P&P state hospice Providers must submit the DHCS hospice election and addendum forms... to the Member's respective MCP...?

Answer: YES

Source: GG.1503, Page 7 and 10

57. Does the P&P state that per Medicare policy... general inpatient care may be required for procedures necessary for pain control... and is not equivalent to a hospital level of care...?

Answer: YES

Source: GG.1503, Pages 8-9, Sections III.D and III.E

58. Does the P&P include the five listed services not covered by a hospice Provider?

Answer: NO

59. Does the P&P state MCPs are reminded to remain proactive and vigilant regarding program integrity requirements...?

Answer: NO

60. Does the P&P state DHCS expects MCPs to apply appropriate compliance review protocols... upon receipt of a hospice election form...?

Answer: NO

61. Does the P&P state DHCS places an indicator in the Medi-Cal Eligibility Data System... with a "900" restricted services code...?

Answer: NO

62. Does the P&P state MCPs must examine documentation received from the hospice Provider to determine the qualification of the Member... and not based on fraudulent submissions?

Answer: YES

Source: GG.1503, Pages 3-5, 8-10, Sections II.F, III.A, III.D, and III.F

63. Does the P&P acknowledge MCPs are still contractually obligated to report complete... Encounter Data... specifically referring Provider, rendering Provider, and starting day of service?

Answer: NO

64. Does the P&P state that at any time, DHCS may inspect and audit MCP records, documents, and electronic systems...?

Answer: YES

Source: HH.2022, Page 2, Section II.C
```

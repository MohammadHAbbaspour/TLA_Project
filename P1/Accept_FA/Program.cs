using System;
using System.Collections.Generic;
using System.Linq;

namespace Accept_FA
{
    public class State
    {
        public string Name;
        public Dictionary<string, List<State>> Transitions;
        public State(string name)
        {
            this.Name = name;
            this.Transitions = new Dictionary<string, List<State>>();
        }

        public void Add_Transition(string name, State state)
        {
            if(!this.Transitions.ContainsKey(name))
                this.Transitions.Add(name, new List<State>());
            this.Transitions[name].Add(state);
        }

        public List<State> Get_Transition_State(string alphabet)
        {
            return this.Transitions[alphabet];
        }
    }

    public class NFA
    {
        public List<State> States;
        public List<string> Alphabet;
        public State Initial_State;
        public List<State> Final_States;

        public NFA(List<string> alphabets)
        {
            this.States = new List<State>();
            this.Alphabet = alphabets;
            this.Final_States = new List<State>();
        }

        public void Add_State(string name)
        {
            this.States.Add(new State(name));
        }

        public void Set_Initial_State(string name)
        {
            this.Initial_State = this.States.Where(state => state.Name == name).FirstOrDefault();
        }

        public void Add_Final_State(string name)
        {
            this.Final_States.Add(this.States.Where(state => state.Name == name).FirstOrDefault());
        }

        public void Add_Transition(string s, string a, string dest)
        {
            State start = this.States.Where(state => state.Name == s).FirstOrDefault();
            State destination = this.States.Where(state => state.Name == dest).FirstOrDefault();
            start.Add_Transition(a, destination);
        }

        public bool Check_String(State start, int i, string str)
        {
            if(i >= str.Length)
            {
                if(this.Final_States.Contains(start))
                    return true;
                return false;
            }
            bool accepted = false;
            List<State> next_states;
            if(start.Transitions.ContainsKey("$"))
            {
                next_states = start.Get_Transition_State("$");
                foreach(var state in next_states)
                {
                    accepted = Check_String(state, i, str);
                    if(accepted)
                        break;
                }
            }
            if(!accepted)
            {
                if(!start.Transitions.ContainsKey(str[i].ToString()))
                    return accepted;
                next_states = start.Get_Transition_State(str[i].ToString());
                foreach(var state in next_states)
                {
                    accepted = Check_String(state, i + 1, str);
                    if(accepted)
                        break;
                }
            }
            return accepted;
        }

    }
    class Program
    {
        static void Main(string[] args)
        {
            var states = Console.ReadLine().Split(new char[]{',', '{', '}'}, StringSplitOptions.RemoveEmptyEntries).ToArray();
            var alphabets = Console.ReadLine().Split(new char[]{',', '{', '}'}, StringSplitOptions.RemoveEmptyEntries).ToList();
            NFA nfa = new NFA(alphabets);
            foreach(var state in states)
                nfa.Add_State(state);
            nfa.Set_Initial_State(states[0]);
            var final_states = Console.ReadLine().Split(new char[]{',', '{', '}'}, StringSplitOptions.RemoveEmptyEntries).ToArray();
            foreach(var state in final_states)
                nfa.Add_Final_State(state);
            int transition_count = int.Parse(Console.ReadLine());
            for(int _ = 0; _ < transition_count; _++)
            {
                var transition = Console.ReadLine().Split(',');
                nfa.Add_Transition(transition[0], transition[1], transition[2]);
            }
            string str = Console.ReadLine();
            if(nfa.Check_String(nfa.Initial_State, 0, str))
                System.Console.WriteLine("Accepted");
            else
                System.Console.WriteLine("Rejected");
        }
    }
}
